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

    # Step 2: Find all harvested records_*.jsonl files
    jsonl_files = sorted(glob.glob(os.path.join(OUTPUT_DIR, "records_*.jsonl")))

    if not jsonl_files:
        print("❌ No harvested records files found.")
        exit(1)

    # Step 3: Load and deduplicate all records across files
    seen = set()
    records = []

    print(f"📂 Found {len(jsonl_files)} .jsonl files. Deduplicating across all...")

    for file in jsonl_files:
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                record = json.loads(line)
                uid = record.get("link") or record.get("title")
                if uid and uid not in seen:
                    seen.add(uid)
                    records.append(record)

    print(f"🧹 Loaded {len(records)} unique records after deduplicating across all batches.")

    # Step 4: Build FAISS index
    build_faiss_index(records, index_path=INDEX_OUTPUT, metadata_path=METADATA_OUTPUT)
