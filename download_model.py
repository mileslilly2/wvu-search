# guaranteed_model_download.py
from sentence_transformers import SentenceTransformer
import os

model_name = "all-MiniLM-L6-v2"
save_dir = os.path.join("models", model_name)
os.makedirs(save_dir, exist_ok=True)

model = SentenceTransformer(model_name)

# SentenceTransformer wrapper (pooling, normalization, etc.)
model.save(save_dir)

# Explicitly save the Hugging Face transformer (this downloads pytorch_model.bin)
transformer_model = model._first_module().auto_model
print(transformer_model.config)
print(transformer_model.state_dict())
# Save the transformer model
transformer_model.save_pretrained(save_dir)
print("Transformer model saved.")
print(transformer_model)
# Save the tokenizer

# Explicitly save the tokenizer files
tokenizer = model.tokenizer
tokenizer.save_pretrained(save_dir)

print(f"✅ Everything downloaded and saved in: {save_dir}")
