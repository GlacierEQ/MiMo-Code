#!/usr/bin/env python3
import os
import re
import datetime
from pathlib import Path

# Paths
HOME_DIR = Path.home()
INPUT_FILE = HOME_DIR / "CASE_STRUCTURE/MEM0_ACTIVE_CONTEXT.md"
OUTPUT_FILE = HOME_DIR / "CASE_STRUCTURE/MEM0_ACTIVE_CONTEXT_ORGANIZED.md"

def parse_facts(file_path):
    if not file_path.exists():
        print(f"Error: {file_path} does not exist.")
        return []

    content = file_path.read_text(encoding="utf-8")
    
    # Split content by Fact Nodes
    # Nodes typically start with: ### [number]. Fact Node `[node_id]`
    node_pattern = re.compile(
        r"###\s+(?P<index>\d+)\.\s+Fact\s+Node\s+`\[(?P<id>[a-f0-9]+)\]`[\r\n]+"
        r"-\s+\*\*Fact\*\*:\s+(?P<fact>.+?)[\r\n]+"
        r"(?:-\s+\*\*Categories\*\*:\s+(?P<categories>.+?)[\r\n]+)?"
        r"(?:-\s+\*\*Created\*\*:\s+(?P<created>.+?)(?:[\r\n]+|$))?",
        re.DOTALL
    )
    
    facts = []
    for match in node_pattern.finditer(content):
        group_dict = match.groupdict()
        fact_text = group_dict["fact"].strip().replace("\n", " ")
        categories_str = group_dict["categories"] or "Uncategorized"
        categories = [c.strip() for c in categories_str.split(",")]
        created = group_dict["created"] or "Unknown"
        
        facts.append({
            "index": int(group_dict["index"]),
            "id": group_dict["id"],
            "fact": fact_text,
            "categories": categories,
            "created": created
        })
        
    return facts

def categorize_facts(facts):
    categories = {
        "federal_claims": {
            "title": "⚖️ I. Federal Statutory & Constitutional Claims",
            "desc": "Claims of constitutional violations under 42 U.S.C. §§ 1983, 1985, and federal criminal offenses (18 U.S.C. §§ 1001, 1512, 1519, 241, 242) concerning due process, equal protection, conspiracy, and evidence tampering.",
            "keywords": ["1983", "1985", "18 usc", "usc §", "amendment", "constitutional", "color of law", "due process", "equal protection", "lugar v. edmondson", "conspiracy against rights"],
            "items": []
        },
        "fraud_matrix": {
            "title": "🌀 II. Procedural & Jurisdictional Fraud Matrices (F-001 to F-010)",
            "desc": "Orchestrated structural anomalies, notice defects, predetermined orders, stay violations, Rule 58 violations, and extended void TRO enforcement timelines.",
            "keywords": ["fraud event", "procedural fraud matrix", "f-00", "f-01", "contempt trap", "stay motion", "rule 58", "statutory expiration", "predetermined", "backdating", "60-second", "87-second", "ambush hearing", "retroactive", "tampering"],
            "items": []
        },
        "exhibits": {
            "title": "📁 III. Evidentiary Exhibit Master Mappings",
            "desc": "Assigned case exhibits (Exhibits A through L) verifying specific dockets, timestamps, mail/phone receipts, and statistical ruling patterns.",
            "keywords": ["required case exhibit", "exhibit a", "exhibit b", "exhibit c", "exhibit d", "exhibit e", "exhibit f", "exhibit g", "exhibit h", "exhibit i", "exhibit j", "exhibit k", "exhibit l"],
            "items": []
        },
        "family_court": {
            "title": "🧍‍♂️ IV. Family Court Proceeding Context & Sibling Claims",
            "desc": "Kapolei Family Court dockets, related case codes (1FDV, 1FDA), supervision mandates (PACT), Family Wizard settings, and domestic details (residences, firearms provisions, Chico).",
            "keywords": ["kapolei", "family court", "1fda", "1fdv", "visitation", "pact", "family wizard", "teresa", "brower", "shaw", "protective order", "liliha", "chico", "dog", "firearms", "petitioner", "respondent"],
            "items": []
        },
        "infrastructure": {
            "title": "🤖 V. Autonomous Infrastructure & Swarm Configurations",
            "desc": "APEX control plane settings, Goose swarm configurations, MotherDuck/Supabase/Notion synchronization pipelines, and zero-operation workflows.",
            "keywords": ["apex", "aspen grove", "goose", "swarm", "connector", "notion", "supabase", "motherduck", "daemon", "l1", "l2", "l3", "l4", "l5", "l6", "agent", "rust-based"],
            "items": []
        },
        "uncategorized": {
            "title": "📝 VI. General Fact Records & Case Context",
            "desc": "Additional background items and general litigation notes synced from Mem0.",
            "keywords": [],
            "items": []
        }
    }
    
    for f in facts:
        fact_lower = f["fact"].lower()
        matched = False
        
        # Check against categories in order of precedence
        for key in ["federal_claims", "fraud_matrix", "exhibits", "family_court", "infrastructure"]:
            if any(kw in fact_lower for kw in categories[key]["keywords"]):
                categories[key]["items"].append(f)
                matched = True
                break
                
        if not matched:
            categories["uncategorized"]["items"].append(f)
            
    return categories

def write_organized_markdown(categories, total_facts, output_path):
    now = datetime.datetime.now(datetime.UTC).isoformat()
    
    sections = []
    sections.append("# 🧠 Organized Litigation Memories (Active Mem0 Stack)")
    sections.append(f"\n*Last updated & categorized: `{now}`*")
    sections.append("\nThis document contains the 100 litigation facts synced from the Mem0 Cloud system, systematically indexed and categorized for obsidian importing and pleading compilation.")
    
    # ── Summary Dashboard ──
    sections.append("\n## 📊 Memory Distribution Dashboard")
    sections.append("\n| Category | Count | Description |")
    sections.append("| :--- | :---: | :--- |")
    for key, val in categories.items():
        sections.append(f"| [{val['title']}]({output_path.name}#user-content-{key}) | **{len(val['items'])}** | {val['desc'][:80]}... |")
    sections.append(f"| **Total Active Facts** | **{total_facts}** | **100% of synced memories accounted for** |")

    # ── Categories breakdown ──
    for key, val in categories.items():
        sections.append(f"\n<a name=\"{key}\"></a>")
        sections.append(f"## {val['title']}")
        sections.append(f"*{val['desc']}*")
        sections.append("\n---")
        
        if not val["items"]:
            sections.append("\n*No facts matched this category.*")
            continue
            
        for item in val["items"]:
            # Format categories nicely
            cats_badges = " ".join([f"`{c}`" for c in item["categories"]])
            sections.append(
                f"\n### Fact Node `[{item['id']}]` (Fact #{item['index']})\n"
                f"- **Fact**: {item['fact']}\n"
                f"- **Categories**: {cats_badges}\n"
                f"- **Created**: `{item['created']}`"
            )
            
    output_path.write_text("\n".join(sections), encoding="utf-8")
    print(f"✅ Success: Organized memories written to {output_path}")

def main():
    print("⏳ Parsing facts...")
    facts = parse_facts(INPUT_FILE)
    if not facts:
        print("❌ FAILED: No facts parsed.")
        return
        
    print(f"🔍 Loaded {len(facts)} facts. Categorizing...")
    categories = categorize_facts(facts)
    
    print("✍️ Generating organized markdown...")
    write_organized_markdown(categories, len(facts), OUTPUT_FILE)

if __name__ == "__main__":
    main()
