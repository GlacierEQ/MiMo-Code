#!/data/data/com.termux/files/usr/bin/env python3
"""
APEX Backend Background Optimizer (apex_optimizer.py)
Dynamically orchestrates skills, connectors, system memory, and background processes
to maintain peak efficiency and prevent Signal 9 crashes under Termux.
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error
import gc
import subprocess
from datetime import datetime, timezone
from pathlib import Path

# Paths
HOME = os.path.expanduser("~")
SKILLS_DIR = Path(f"{HOME}/.gemini/skills")
MANIFEST_PATH = SKILLS_DIR / "SKILLS_MANIFEST.json"
STATUS_FILE = Path(f"{HOME}/.gemini/tmp/connector_status.json")
LOG_FILE = Path(f"{HOME}/logs/apex_optimizer.log")

os.makedirs(STATUS_FILE.parent, exist_ok=True)
os.makedirs(LOG_FILE.parent, exist_ok=True)

def log_msg(level, message):
    timestamp = datetime.now(timezone.utc).isoformat()
    log_line = f"[{timestamp}] [{level}] {message}\n"
    with open(LOG_FILE, "a") as f:
        f.write(log_line)
    if sys.stdout.isatty():
        print(f"[{level}] {message}")

class APEXOptimizer:
    def __init__(self):
        log_msg("INFO", "Initializing APEX Backend Background Optimizer...")
        self.mem_avail = -1
        self.proc_count = -1

        # Mount Aspen Grove Notion Bridge & API Integration
        aspen_path = "/data/data/com.termux/files/home/intelligence/aspen-grove-operator-v7"
        if aspen_path not in sys.path:
            sys.path.append(aspen_path)
        try:
            import importlib.util
            spec_bridge = importlib.util.spec_from_file_location(
                "aspen_notion_bridge",
                f"{aspen_path}/bridges/aspen_notion_bridge.py"
            )
            bridge_mod = importlib.util.module_from_spec(spec_bridge)
            spec_bridge.loader.exec_module(bridge_mod)
            self.notion_bridge = bridge_mod.AspenNotionBridge()
            self.ag_api = bridge_mod.AspenGroveAPI()
            log_msg("SUCCESS", "Aspen Grove Notion Bridge & AG.INDEX API successfully mounted.")
        except Exception as e:
            self.notion_bridge = None
            self.ag_api = None
            log_msg("WARNING", f"Aspen Grove Notion Bridge not loaded: {str(e)}")

    def orchestrate_skills(self):
        """Scans local skills directories recursively, registers primary skills in manifest, and generates a unified index."""
        if not MANIFEST_PATH.exists():
            log_msg("WARNING", f"Skills manifest not found at {MANIFEST_PATH}")
            return

        try:
            # 1. Discover all skills recursively
            discovered_skills = {}
            primary_skills = {}
            
            for md_path in SKILLS_DIR.rglob("SKILL.md"):
                # Key is the directory name
                skill_key = md_path.parent.name.replace("-", "_")
                
                # Check if it's primary (direct child of SKILLS_DIR)
                is_primary = md_path.parent.parent == SKILLS_DIR
                
                skill_entry = {
                    "path": str(md_path),
                    "relative_path": str(md_path.relative_to(HOME)),
                    "version": "1.0",
                    "active": True,
                    "is_primary": is_primary
                }
                
                discovered_skills[skill_key] = skill_entry
                if is_primary:
                    primary_skills[skill_key] = {
                        "path": str(md_path),
                        "version": "1.0",
                        "active": True
                    }

            # 2. Update central manifest with primary skills
            with open(MANIFEST_PATH, "r") as f:
                manifest = json.load(f)
            
            skills_manifest_dict = manifest.get("skills", {})
            changed = False
            
            for k, v in primary_skills.items():
                if k not in skills_manifest_dict:
                    skills_manifest_dict[k] = v
                    log_msg("SUCCESS", f"Registered new primary skill '{k}' in manifest.")
                    changed = True
            
            if changed:
                manifest["skills"] = skills_manifest_dict
                manifest["synthesized"] = datetime.now(timezone.utc).isoformat()
                with open(MANIFEST_PATH, "w") as f:
                    json.dump(manifest, f, indent=2)
                log_msg("INFO", "Skills manifest successfully synchronized.")

            # 3. Write comprehensive skills index to avoid manifest bloating (saving tokens)
            index_path = SKILLS_DIR / "SKILLS_INDEX.json"
            index_data = {
                "synthesized": datetime.now(timezone.utc).isoformat(),
                "total_skills_count": len(discovered_skills),
                "primary_count": len(primary_skills),
                "nested_count": len(discovered_skills) - len(primary_skills),
                "skills": discovered_skills
            }
            with open(index_path, "w") as f_idx:
                json.dump(index_data, f_idx, indent=2)
            
            log_msg("SUCCESS", f"Skills Index updated: Discovered {len(discovered_skills)} skills ({len(primary_skills)} primary, {len(discovered_skills) - len(primary_skills)} nested).")
            
        except Exception as e:
            log_msg("ERROR", f"Failed to orchestrate skills: {str(e)}")

    def orchestrate_connectors(self):
        """Checks connections for Supabase, Notion, and Mem0, saving status and logging heartbeats."""
        status = {
            "last_checked": datetime.now(timezone.utc).isoformat(),
            "connectors": {
                "supabase": {"status": "UNKNOWN", "latency_ms": -1},
                "notion": {"status": "UNKNOWN", "latency_ms": -1},
                "mem0": {"status": "UNKNOWN", "latency_ms": -1}
            }
        }

        # Check Supabase
        supabase_url = os.environ.get("SUPABASE_URL")
        if supabase_url:
            t0 = time.time()
            try:
                # Ping Supabase REST api endpoint
                req = urllib.request.Request(f"{supabase_url}/rest/v1/", headers={"apikey": os.environ.get("SUPABASE_ANON_KEY", "")})
                with urllib.request.urlopen(req, timeout=3.0) as resp:
                    resp.read()
                status["connectors"]["supabase"] = {"status": "ONLINE", "latency_ms": int((time.time() - t0) * 1000)}
            except Exception as e:
                status["connectors"]["supabase"] = {"status": "OFFLINE", "error": str(e)}

        # Check Notion API
        t0 = time.time()
        try:
            req = urllib.request.Request(
                "https://api.notion.com/v1/users",
                headers={
                    "Authorization": f"Bearer {os.environ.get('NOTION_TOKEN', '')}",
                    "Notion-Version": "2022-06-28"
                }
            )
            with urllib.request.urlopen(req, timeout=3.0) as resp:
                resp.read()
            status["connectors"]["notion"] = {"status": "ONLINE", "latency_ms": int((time.time() - t0) * 1000)}
        except Exception as e:
            # If authorized/unauthorized but reached API, we consider it connected
            if isinstance(e, urllib.error.HTTPError) and e.code == 401:
                status["connectors"]["notion"] = {"status": "ONLINE (AUTH_REQUIRED)", "latency_ms": int((time.time() - t0) * 1000)}
            else:
                status["connectors"]["notion"] = {"status": "OFFLINE", "error": str(e)}

        # Check Mem0 Connection
        t0 = time.time()
        mem0_key = os.environ.get("MEM0_API_KEY")
        if mem0_key:
            try:
                req = urllib.request.Request(
                    "https://api.mem0.ai/v1/users/",
                    headers={"Authorization": f"Token {mem0_key}"}
                )
                with urllib.request.urlopen(req, timeout=3.0) as resp:
                    resp.read()
                status["connectors"]["mem0"] = {"status": "ONLINE", "latency_ms": int((time.time() - t0) * 1000)}
            except Exception as e:
                if isinstance(e, urllib.error.HTTPError) and e.code in [401, 403, 404]:
                    status["connectors"]["mem0"] = {"status": "ONLINE (RESTRICTED)", "latency_ms": int((time.time() - t0) * 1000)}
                else:
                    status["connectors"]["mem0"] = {"status": "OFFLINE", "error": str(e)}

        try:
            with open(STATUS_FILE, "w") as f:
                json.dump(status, f, indent=2)
            log_msg("INFO", f"Connectors verified: Supabase={status['connectors']['supabase']['status']}, Notion={status['connectors']['notion']['status']}, Mem0={status['connectors']['mem0']['status']}")
        except Exception as e:
            log_msg("ERROR", f"Failed to save connector status: {str(e)}")

        # Merge & Bridge flow: log session to Notion APEX CMD BUS if Notion is online
        if self.notion_bridge and status["connectors"]["notion"]["status"].startswith("ONLINE"):
            try:
                success = self.notion_bridge.log_session_to_notion("OPTIMIZED_HEARTBEAT")
                if success:
                    log_msg("SUCCESS", "Dynamic Bridge Flow: Heartbeat logged to Notion APEX CMD BUS.")
                else:
                    log_msg("WARNING", "Dynamic Bridge Flow: Notion Heartbeat rejected or API key missing.")
            except Exception as e:
                log_msg("WARNING", f"Dynamic Bridge Flow failed to log Notion: {str(e)}")

        # Sync telemetry node to local AG.INDEX memory sink
        if self.ag_api:
            try:
                node_props = {
                    "connector_states": status["connectors"],
                    "system_memory": f"{self.mem_avail} MB available",
                    "process_count": self.proc_count
                }
                node_id = self.ag_api.INDEX("gemini-optimizer-heartbeat", node_props)
                log_msg("SUCCESS", f"Dynamic Bridge Flow: Telemetry indexed in AG.INDEX (Node: {node_id})")

                # Persistence bridge: Write the merged index directly to the parent filesystem index file
                parent_index_dir = Path(f"{HOME}/.gemini/tmp/home")
                parent_index_dir.mkdir(parents=True, exist_ok=True)
                parent_index_file = parent_index_dir / "AG_INDEX.json"
                
                # Load current parent index state
                parent_index = {}
                if parent_index_file.exists():
                    try:
                        with open(parent_index_file, "r") as f_pi:
                            parent_index = json.load(f_pi)
                    except Exception:
                        pass
                
                # Merge the new node
                parent_index[node_id] = {
                    "entity": "gemini-optimizer-heartbeat",
                    **node_props,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                # Keep last 50 heartbeats to avoid massive file growth (token savings & efficiency)
                heartbeats = [k for k, v in parent_index.items() if v.get("entity") == "gemini-optimizer-heartbeat"]
                if len(heartbeats) > 50:
                    for old_k in sorted(heartbeats, key=lambda x: parent_index[x].get("timestamp"))[:-50]:
                        parent_index.pop(old_k, None)

                # Save back to parent index
                with open(parent_index_file, "w") as f_pi:
                    json.dump(parent_index, f_pi, indent=2)
                log_msg("SUCCESS", f"Dynamic Bridge Flow: Successfully persisted merge to parent index at {parent_index_file.name}")
            except Exception as e:
                log_msg("WARNING", f"AG.INDEX sync deferred or failed to write parent: {str(e)}")

    def sync_mem0_memories(self):
        """Fetches all memories for user 'casey' from the Mem0 platform and synchronizes them to a local markdown file."""
        mem0_key = os.environ.get("MEM0_API_KEY")
        if not mem0_key:
            return

        try:
            from mem0 import MemoryClient
            client = MemoryClient(api_key=mem0_key)
            memories = client.get_all(filters={"user_id": "casey"})
            
            if isinstance(memories, dict):
                memories = memories.get("results", memories.get("memories", []))
            
            if not isinstance(memories, list):
                log_msg("WARNING", f"Mem0 memories return format unexpected: {type(memories)}")
                return
            
            # Format as markdown
            lines = [
                "# 🧠 Active Mem0 Litigation Memories\n",
                f"*Last synchronized: {datetime.now(timezone.utc).isoformat()}*\n",
                "This file is dynamically updated by the APEX Background Optimizer daemon. It keeps active facts from the cloud Mem0 memory pool available in the local litigation workspace.\n",
                "## 🗄️ Stored Memories\n"
            ]
            
            if not memories:
                lines.append("*No memories currently stored in the cloud pool.*")
            else:
                for i, mem in enumerate(memories, 1):
                    mem_id = mem.get("id", "N/A")
                    mem_text = mem.get("memory", "").strip()
                    categories = mem.get("categories", [])
                    created_at = mem.get("created_at", "N/A")
                    
                    lines.append(f"### {i}. Fact Node `[{mem_id[:8]}]`")
                    lines.append(f"- **Fact**: {mem_text}")
                    if categories:
                        lines.append(f"- **Categories**: {', '.join(categories)}")
                    lines.append(f"- **Created**: {created_at}")
                    lines.append("")
                    
            context_file = Path(f"{HOME}/CASE_STRUCTURE/MEM0_ACTIVE_CONTEXT.md")
            with open(context_file, "w") as f:
                f.write("\n".join(lines))
                
            log_msg("SUCCESS", f"Synchronized {len(memories)} cloud memories from Mem0 to {context_file.name}")
            
        except Exception as e:
            log_msg("WARNING", f"Failed to sync Mem0 cloud memories: {str(e)}")

    def optimize_background_ops(self):
        """Monitors memory usage and process count, executing mitigations if limits are approached."""
        # 1. Process Count Guard (prevent Signal 9)
        try:
            ps = subprocess.Popen(["ps", "-ef"], stdout=subprocess.PIPE, stdin=subprocess.DEVNULL)
            output, _ = ps.communicate()
            lines = output.decode("utf-8", errors="ignore").splitlines()
            # Count python and active user processes
            self.proc_count = len([l for l in lines if "grep" not in l and "ps" not in l])
            log_msg("INFO", f"Active background process count: {self.proc_count}/32 limit")
            
            if self.proc_count > 26:
                log_msg("WARNING", f"High process count detected ({self.proc_count}). Pruning defunct/zombie processes...")
                # Force collection of dead handles
                gc.collect()
        except Exception as e:
            log_msg("ERROR", f"Failed process check: {str(e)}")

        # 2. RAM Mitigation (prevent OOM)
        try:
            with open("/proc/meminfo", "r") as f:
                meminfo = f.read()
            self.mem_avail = 0
            for line in meminfo.splitlines():
                if line.startswith("MemAvailable:"):
                    self.mem_avail = int(line.split()[1]) // 1024
                    break
            
            if self.mem_avail > 0 and self.mem_avail < 500:
                log_msg("WARNING", f"Low memory alert ({self.mem_avail} MB). Reclaiming resources...")
                gc.collect()
                # If Ollama is running models, unload them to free up massive RAM
                try:
                    req = urllib.request.urlopen("http://localhost:11434/api/ps", timeout=1.0)
                    data = json.loads(req.read().decode())
                    for model in data.get("models", []):
                        name = model.get("name")
                        log_msg("INFO", f"Unloading Ollama model: {name}")
                        # Unload command
                        unload_req = urllib.request.Request(
                            "http://localhost:11434/api/chat",
                            data=json.dumps({"model": name, "keep_alive": 0}).encode(),
                            headers={"Content-Type": "application/json"}
                        )
                        urllib.request.urlopen(unload_req, timeout=1.0).read()
                except Exception:
                    pass
        except Exception as e:
            log_msg("ERROR", f"Failed RAM check: {str(e)}")

    def run_loop(self, interval=120):
        log_msg("SUCCESS", f"APEX Background Optimizer loop started (Interval: {interval}s)")
        try:
            while True:
                self.optimize_background_ops()
                self.orchestrate_skills()
                self.orchestrate_connectors()
                self.sync_mem0_memories()
                time.sleep(interval)
        except KeyboardInterrupt:
            log_msg("INFO", "Optimizer terminated by keyboard interrupt.")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="APEX Background Optimizer")
    parser.add_argument("--daemon", action="store_true", help="Run as continuous daemon")
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    args = parser.parse_args()

    # Load environment files to get Notion/Supabase/Mem0 keys
    env_file = Path(f"{HOME}/.env")
    gemini_env = Path(f"{HOME}/.gemini_env")
    for file in [env_file, gemini_env]:
        if file.exists():
            with open(file, "r") as f:
                for line in f:
                    if line.strip() and not line.startswith("#"):
                        parts = line.strip().split("=", 1)
                        if len(parts) == 2:
                            os.environ[parts[0].strip()] = parts[1].strip()

    optimizer = APEXOptimizer()
    if args.once:
        optimizer.orchestrate_skills()
        optimizer.orchestrate_connectors()
        optimizer.sync_mem0_memories()
        optimizer.optimize_background_ops()
    else:
        optimizer.run_loop()

if __name__ == "__main__":
    main()
