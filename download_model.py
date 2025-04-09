from transformers import AutoModel, AutoTokenizer
import os

model_name = "sentence-transformers/all-MiniLM-L6-v2"
save_dir = os.path.join("models", "all-MiniLM-L6-v2")
os.makedirs(save_dir, exist_ok=True)

# Force Hugging Face to download the .bin PyTorch checkpoint
model = AutoModel.from_pretrained("models/all-MiniLM-L6-v2", 
                                  local_files_only=True,
                                  from_safetensors=True)

tokenizer = AutoTokenizer.from_pretrained(model_name)

model.save_pretrained(save_dir)
tokenizer.save_pretrained(save_dir)

print(f"✅ PyTorch .bin weights saved in: {save_dir}")
