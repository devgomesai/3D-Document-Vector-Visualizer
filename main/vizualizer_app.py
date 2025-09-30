import streamlit as st
import numpy as np
import plotly.express as px
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.manifold import TSNE
import pandas as pd

# ---------- Helpers ----------
def chunk_text(text, chunk_size=200, overlap=50):
    """Split text into chunks with optional overlap"""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        if chunk.strip():
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def process_chunks(chunks):
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(chunks)
    return tfidf_matrix, vectorizer

def tsne_3d_plotly(matrix, labels, query_point=None):
    n_samples = matrix.shape[0]
    if n_samples < 2:
        st.warning("Not enough data to plot t-SNE. Add more text chunks.")
        return

    perplexity = min(30, n_samples - 1)
    tsne = TSNE(n_components=3, random_state=42, perplexity=perplexity, learning_rate=100)
    reduced = tsne.fit_transform(matrix.toarray())

    df = pd.DataFrame(reduced, columns=["x", "y", "z"])
    df["label"] = labels

    # Define custom color palette
    color_map = {
        "test1.txt [Chunk 1]": "#00FF00",  # bright green
        "test1.txt [Chunk 2]": "#FFFF00",  # bright yellow
        "test2.txt [Chunk 1]": "#FF00FF",  # magenta
        "test2.txt [Chunk 2]": "#00FFFF",  # cyan
    }

    fig = px.scatter_3d(
        df, x="x", y="y", z="z",
        color="label",
        color_discrete_map=color_map,
        opacity=0.8,
        size_max=8
    )

    if query_point is not None:
        fig.add_scatter3d(
            x=[query_point[0]], y=[query_point[1]], z=[query_point[2]],
            mode="markers+text",
            marker=dict(size=10, color="red", symbol="diamond"),
            name="Query", text=["Query"]
        )

    fig.update_traces(marker=dict(line=dict(width=1, color='black')))  # outline

    config = {"displaylogo": False, "responsive": True}
    st.plotly_chart(fig, config=config, use_container_width=True)



def find_similar_chunks(query, vectorizer, tfidf_matrix, chunks, chunk_names):
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    ranked_indices = similarities.argsort()[::-1]
    results = [(chunk_names[i], chunks[i], similarities[i]) for i in ranked_indices[:5]]
    return results, query_vec

# ---------- Streamlit App ----------
st.title("📄 3D Document VectorVisualizer")

if "chunks" not in st.session_state:
    st.session_state.chunks = []
    st.session_state.chunk_names = []

uploaded_files = st.file_uploader("Upload documents", type=["txt"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        text = uploaded_file.read().decode("utf-8")
        chunks = chunk_text(text, chunk_size=200, overlap=50)
        for i, chunk in enumerate(chunks, 1):
            st.session_state.chunks.append(chunk)
            st.session_state.chunk_names.append(f"{uploaded_file.name} [Chunk {i}]")

if st.session_state.chunks:
    tfidf_matrix, vectorizer = process_chunks(st.session_state.chunks)

    st.subheader("🔍 Query Chunks")
    query = st.text_input("Enter a query to find similar chunks")

    if query:
        results, query_vec = find_similar_chunks(query, vectorizer, tfidf_matrix,
                                                 st.session_state.chunks,
                                                 st.session_state.chunk_names)

        st.write("**Top matching chunks:**")
        for name, chunk, score in results:
            st.markdown(f"**{name}** (score: {score:.3f})")
            st.write(chunk[:300] + "...\n")

        tsne_3d_plotly(tfidf_matrix, st.session_state.chunk_names, query_vec.toarray()[0])
    else:
        tsne_3d_plotly(tfidf_matrix, st.session_state.chunk_names)

    # ---------- Chunk Browser ----------
    st.subheader("📑 All Chunks (Table Preview)")
    chunk_data = [
        {
            "Chunk ID": i + 1,
            "Source": st.session_state.chunk_names[i],
            "Content": st.session_state.chunks[i][:200] + "..."
        }
        for i in range(len(st.session_state.chunks))
    ]
    st.dataframe(pd.DataFrame(chunk_data), width='stretch', height=500)

