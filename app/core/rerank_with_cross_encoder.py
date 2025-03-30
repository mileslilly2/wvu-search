from sentence_transformers import CrossEncoder
from app.search import search_faiss_index  # Make sure this works in your project structure

def rerank_with_cross_encoder(query, faiss_results, model_name="cross-encoder/ms-marco-MiniLM-L6-v2"):
    """
    Reranks FAISS search results based on semantic intent matching using a cross-encoder.
    
    Args:
        query (str): The user's natural language query.
        faiss_results (list of dict): Results from FAISS (each with 'description' field).
        model_name (str): Hugging Face model to use for reranking.
    
    Returns:
        List of tuples: (result_dict, relevance_score), sorted from most to least relevant.
    """
    print("🔄 Loading cross-encoder model...")
    model = CrossEncoder(model_name)

    print("🔢 Scoring documents...")
    pairs = [(query, r["description"] or "") for r in faiss_results]
    scores = model.predict(pairs)

    reranked = sorted(zip(faiss_results, scores), key=lambda x: x[1], reverse=True)
    return reranked

if __name__ == "__main__":
    # Example query
    query = "What is the impact of coal on health?"

    # Step 1: Search with FAISS
    faiss_results = search_faiss_index(query, top_k=10)

    # Step 2: Rerank with cross-encoder
    reranked_results = rerank_with_cross_encoder(query, faiss_results)

    # Step 3: Display
    print("\n📊 Top Reranked Results:\n")
    for i, (result, score) in enumerate(reranked_results, 1):
        print(f"{i}. 📄 {result['title']} (Score: {score:.2f})")
        print(f"   🔗 {result['link']}")
        print(f"   📝 {result['description'][:300]}...\n")
