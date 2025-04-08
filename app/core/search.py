def search_faiss_index(
    query,
    top_k=5,
    index_path="wvu_index.faiss",
    metadata_path="wvu_metadata.pkl"
):
    """
    Performs a semantic search on the FAISS index for the given query.

    Args:
        query (str): Natural language search query.
        top_k (int): Number of top results to return.
        index_path (str): Path to the saved FAISS index.
        metadata_path (str): Path to the saved metadata (pickle).

    Returns:
        List[dict]: Top matching metadata records with distance scores.
    """
    from sentence_transformers import SentenceTransformer
    import faiss
    import numpy as np
    import pickle

    # Load model, FAISS index, and metadata
    model = SentenceTransformer("models/all-MiniLM-L6-v2")

    index = faiss.read_index(index_path)

    with open(metadata_path, "rb") as f:
        metadata = pickle.load(f)

    # Encode query
    query_vector = model.encode([query])
    distances, indices = index.search(np.array(query_vector), top_k)

    results = []
    for idx, score in zip(indices[0], distances[0]):
        record = metadata[idx]
        result = {
            "title": record.get("title", ""),
            "description": record.get("description", ""),
            "link": record.get("link", ""),
            "score": float(score)
        }
        results.append(result)

    return results
