import os
import glob
import json

from app.core.indexer import build_faiss_index
from app.core.time_batch_harvest import harvest_for_duration

# -------------------------
# Configurable parameters
# -------------------------
OUTPUT_DIR = "harvested"
INDEX_OUTPUT = "data/wvu_index.faiss"
METADATA_OUTPUT = "data/wvu_metadata.pkl"
MAX_MINUTES = 30  # How long to harvest

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)

    # Step 1: Run time-based harvest
    harvest_for_duration(output_dir=OUTPUT_DIR, metadata_prefix="oai_dc", max_minutes=MAX_MINUTES)

    # Step 2: Find latest records_*.jsonl file
    jsonl_files = sorted(glob.glob(os.path.join(OUTPUT_DIR, "records_*.jsonl")), reverse=True)
    if not jsonl_files:
        print("❌ No harvested records file found.")
        exit(1)

    latest_jsonl = jsonl_files[0]
    print(f"📄 Loading records from: {latest_jsonl}")

    # Step 3: Load records into memory
    with open(latest_jsonl, "r", encoding="utf-8") as f:
        records = [json.loads(line) for line in f]

    # Step 4: Build FAISS index
    build_faiss_index(records, index_path=INDEX_OUTPUT, metadata_path=METADATA_OUTPUT)
