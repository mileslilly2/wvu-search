from sentence_transformers import SentenceTransformer
import os

model_name = "all-MiniLM-L6-v2"
model = SentenceTransformer(model_name)

# Save the SentenceTransformer model (this saves Pooling/Normalize)
model.save("models/all-MiniLM-L6-v2")

# Save the Hugging Face transformer model part too
transformer_model = model._first_module().auto_model
tokenizer = model.tokenizer

transformer_model.save_pretrained("models/all-MiniLM-L6-v2")
tokenizer.save_pretrained("models/all-MiniLM-L6-v2")

print("✅ Full model saved with config, weights, tokenizer, and pooling layers.")
