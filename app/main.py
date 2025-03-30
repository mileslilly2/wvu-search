from app.search import search_faiss_index

def main():
    print("\n🔍 WVU Semantic Search CLI")
    print("--------------------------")

    while True:
        query = input("\nEnter your search query (or type 'exit'): ").strip()
        if query.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break

        year = input("Filter by year (optional): ").strip() or None
        subject = input("Filter by subject (optional): ").strip() or None

        print("\nSearching...\n")
        results = search_faiss_index(
            query=query,
            top_k=5,
            year_filter=year,
            subject_filter=subject
        )

        if not results:
            print("⚠️  No results found.")
        else:
            for i, result in enumerate(results, 1):
                print(f"{i}. 📄 {result['title']} ({result['year']})")
                print(f"   🔗 {result['link']}")
                print(f"   🧠 Score: {result['score']:.2f}")
                print(f"   📚 Subjects: {', '.join(result['subject'])}")
                print(f"   📝 {result['description'][:300]}...\n")

if __name__ == "__main__":
    main()
