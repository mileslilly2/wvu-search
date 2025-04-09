import requests
import xml.etree.ElementTree as ET
import json
import time
import os
from datetime import datetime

BASE_URL = "https://researchrepository.wvu.edu/do/oai/"
NAMESPACE = {
    "oai": "http://www.openarchives.org/OAI/2.0/",
    "dc": "http://purl.org/dc/elements/1.1/"
}

def parse_record(record):
    title = record.find(".//dc:title", NAMESPACE)
    creators = record.findall(".//dc:creator", NAMESPACE)
    description = record.find(".//dc:description", NAMESPACE)
    date = record.find(".//dc:date", NAMESPACE)
    identifier = record.find(".//dc:identifier", NAMESPACE)
    subject = record.findall(".//dc:subject", NAMESPACE)

    return {
        "title": title.text if title is not None else None,
        "creators": [c.text for c in creators],
        "description": description.text if description is not None else None,
        "link": identifier.text.strip() if identifier is not None else "",
        "subject": [s.text for s in subject],
        "date": date.text if date is not None else None
    }

def harvest_for_duration(output_dir="harvested", metadata_prefix="oai_dc", max_minutes=10):
    os.makedirs(output_dir, exist_ok=True)
    start_time = time.time()
    end_time = start_time + max_minutes * 60
    token_file = os.path.join(output_dir, "resumption_token.txt")
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    jsonl_path = os.path.join(output_dir, f"records_{timestamp}.jsonl")

    # Check if a token exists from a previous session
    if os.path.exists(token_file):
        with open(token_file, "r") as f:
            token = f.read().strip()
        url = f"{BASE_URL}?verb=ListRecords&resumptionToken={token}"
    else:
        url = f"{BASE_URL}?verb=ListRecords&metadataPrefix={metadata_prefix}"

    print(f"🌍 Starting harvest for {max_minutes} minutes...")
    record_count = 0

    with open(jsonl_path, "a", encoding="utf-8") as f_out:
        while url and time.time() < end_time:
            print(f"📥 Fetching: {url}")
            resp = requests.get(url)
            try:
                root = ET.fromstring(resp.content)
            except ET.ParseError as e:
                print("❌ XML ParseError — skipping batch:", e)
                break

            records = root.findall(".//oai:record", NAMESPACE)
            for rec in records:
                parsed = parse_record(rec)
                f_out.write(json.dumps(parsed, ensure_ascii=False) + "\n")
                record_count += 1

            # Handle pagination
            token_elem = root.find(".//oai:resumptionToken", NAMESPACE)
            if token_elem is not None and token_elem.text:
                token = token_elem.text
                url = f"{BASE_URL}?verb=ListRecords&resumptionToken={token}"

                # Save resumption token
                with open(token_file, "w") as f:
                    f.write(token)
            else:
                print("✅ No more resumption token — done.")
                if os.path.exists(token_file):
                    os.remove(token_file)
                break

    print(f"✅ Harvest complete. {record_count} records saved to {jsonl_path}")



harvest_for_duration(output_dir="data/wvu", max_minutes=15)
