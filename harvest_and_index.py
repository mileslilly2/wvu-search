import requests
import xml.etree.ElementTree as ET
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
from tqdm import tqdm
import os

from app.core.indexer import build_faiss_index
from app.core.time_batch_harvest import harvest_for_duration


# -------------------------
# Configurable parameters
# -------------------------
OAI_ENDPOINT = "https://researchrepository.wvu.edu/do/oai/"
METADATA_PREFIX = "oai_dc"
INDEX_OUTPUT = "wvu_index.faiss"
METADATA_OUTPUT = "wvu_metadata.pkl"
MAX_RECORDS = 5000

NAMESPACE = {
    "oai": "http://www.openarchives.org/OAI/2.0/",
    "dc": "http://purl.org/dc/elements/1.1/"
}



if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    records = harvest_for_duration(output_dir="harvested", metadata_prefix="oai_dc", max_minutes=10)
    build_faiss_index(records, index_path="data/wvu_index.faiss", metadata_path="data/wvu_metadata.pkl")
