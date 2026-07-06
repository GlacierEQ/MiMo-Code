import sys
import time

sys.path.append("/data/data/com.termux/files/home/intelligence/aspen-grove-operator-v7")
import importlib.util

spec = importlib.util.spec_from_file_location(
    "mcp_ecosystem_integration",
    "/data/data/com.termux/files/home/intelligence/aspen-grove-operator-v7/mcp_ecosystem_integration.py"
)
mcp_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mcp_mod)

TokenOptimizer = mcp_mod.TokenOptimizer

optimizer = TokenOptimizer()
print("--- Testing Token Optimizer ---")
optimizer.set_cache("query_1_hash", "Cached result for query 1")
time.sleep(1)
result = optimizer.get_cached("query_1_hash")
print(f"Result 1: {result}")
result2 = optimizer.get_cached("query_2_hash")
print(f"Result 2: {result2}")
print("Stats:", optimizer.get_stats())
