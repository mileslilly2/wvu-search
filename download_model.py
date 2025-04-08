# download_model_full.py
from sentence_transformers import SentenceTransformer
import os

model_name = "all-MiniLM-L6-v2"
model = SentenceTransformer(model_name)

# Make sure the save directory exists
save_dir = os.path.join("models", model_name)
os.makedirs(save_dir, exist_ok=True)

# Save the entire SentenceTransformer model (includes tokenizer + transformer)
model.save(save_dir)

# ✅ ALSO save the HuggingFace model directly for full offline support
model._first_module().auto_model.save_pretrained(save_dir)
model.tokenizer.save_pretrained(save_dir)

print(f"✅ Full model saved for offline use at: {save_dir}")
