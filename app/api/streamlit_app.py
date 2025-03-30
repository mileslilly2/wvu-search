import streamlit as st
from search import search_faiss_index

st.set_page_config(page_title="WVU Semantic Search", page_icon="🔍", layout="wide")

st.title("🔍 WVU Semantic Search")
st.caption("Search across WVU research repository with natural language queries.")

with st.form("search_form"):
    query = st.text_input("Enter your question or keywords", placeholder="e.g., economic impact of coal mining")
    submitted = st.form_submit_button("Search")

if submitted and query.strip():
    with st.spinner("Searching..."):
        
        results = search_faiss_index(
            query=query.strip(),
            top_k=5,
            index_path="scripts/data/wvu_index.faiss",
            metadata_path="scripts/data/wvu_metadata.pkl"
            
        )

    if not results:
        st.warning("No results found.")
    else:
        for result in results:
            print(result)
            st.markdown(f"### 📄 [{result['title']}]({result['link']})")
            #st.write(f"**Date:** {result['year']} &nbsp;&nbsp; | &nbsp;&nbsp; **Subjects:** {', '.join(result['subject'])}")
            st.write(f"**Score:** {result['score']:.2f}")
            #st.write(f"**Subjects:** {', '.join(result['subject'])}")
            st.markdown(f"**Summary:**<br>{result['description']}", unsafe_allow_html=True)
            st.markdown("---")
else:
    if submitted:
        st.error("Please enter a search query.")
