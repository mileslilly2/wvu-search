from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
import os
def build_faiss_index(records, index_path="wvu_index.faiss", metadata_path="wvu_metadata.pkl"):
    """
    Builds a FAISS index from a list of metadata records.

    Args:
        records (list of dict): Each record must have 'title', 'description', and 'link' keys.
                                Optional fields: 'year', 'subject'
        index_path (str): File path to save the FAISS index.
        metadata_path (str): File path to save the metadata pickle.

    Returns:
        None (writes files to disk)
    """
    if not records:
        raise ValueError("The 'records' list is empty.")

    # Normalize optional fields
    for record in records:
        record["year"] = record.get("year") or "Unknown"
        subject = record.get("subject")
        if isinstance(subject, str):
            record["subject"] = [subject]
        elif subject is None:
            record["subject"] = []

    # Load sentence transformer model
    model = SentenceTransformer("models/all-MiniLM-L6-v2")  # 384-dim, lightweight and fast

    # Prepare combined text: title + description
    texts = [
        f"{record.get('title', '')}. {record.get('description', '') or ''}"
        for record in records
    ]

    print(f"Encoding {len(texts)} records...")
    embeddings = model.encode(texts, show_progress_bar=True)

    # Build FAISS index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

    # Save index and metadata
    faiss.write_index(index, index_path)
    with open(metadata_path, "wb") as f:
        pickle.dump(records, f)

    print(f"✅ FAISS index and metadata saved to '{index_path}' and '{metadata_path}'.")