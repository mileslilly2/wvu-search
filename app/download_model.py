# download_model.py
from sentence_transformers import SentenceTransformer

model_name = "all-MiniLM-L6-v2"
model = SentenceTransformer(model_name)
model.save("models/all-MiniLM-L6-v2")

print("✅ Model downloaded and saved to models/all-MiniLM-L6-v2/")
