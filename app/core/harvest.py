import requests
import xml.etree.ElementTree as ET
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
from tqdm import tqdm


BASE_URL = "https://researchrepository.wvu.edu/do/oai/"
NAMESPACE = {
    "oai": "http://www.openarchives.org/OAI/2.0/",
    "dc": "http://purl.org/dc/elements/1.1/"
}
aaaa
def harvest_records(metadata_prefix="oai_dc", max_records=50):
    url = f"{OAI_ENDPOINT}?verb=ListRecords&metadataPrefix={metadata_prefix}"
    records = []

    while url and len(records) < max_records:
        print(f"Fetching: {url}")
        resp = requests.get(url)
        try:
            root = ET.fromstring(resp.content)
        except ET.ParseError as e:
            print("❌ XML ParseError — skipping this batch:", e)
            break  # or `continue` to skip and move on

        

        for record in root.findall(".//oai:record", NAMESPACE):
            title = record.find(".//dc:title", NAMESPACE)
            creators = record.findall(".//dc:creator", NAMESPACE)
            description = record.find(".//dc:description", NAMESPACE)
            date = record.find(".//dc:date", NAMESPACE)
            identifier = record.find(".//dc:identifier", NAMESPACE)
            subject = record.findall(".//dc:subject", NAMESPACE)
            

            records.append({
                "title": title.text if title is not None else None,
                "creators": [c.text for c in creators],
                "description": description.text if description is not None else None,
                "link": identifier.text if identifier is not None else None,
                "subject": [s.text for s in subject],
                "link": identifier.text.strip() if identifier is not None else ""
            
            })

        # Pagination
        token = root.find(".//oai:resumptionToken", NAMESPACE)
        if token is not None and token.text:
            url = f"{BASE_URL}?verb=ListRecords&resumptionToken={token.text}"
        else:
            break

    print(f"✅ Harvested {len(records)} records.")
    return records





# Example
if __name__ == "__main__":
    records = harvest_records(max_records=5000)
    #for record in records:
        #print(f"\nTitle: {record['title']}\nBy: {', '.join(record['creators'])}\nLink: {record['link']}\n")
