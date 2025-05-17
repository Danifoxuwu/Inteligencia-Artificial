from transformers import (
    pipeline,
    AutoTokenizer,
    AutoModelForCausalLM
)
from peft import PeftModel
import torch

# 1. Cargar modelo base y tokenizer
model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(model_id)
base_model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float32  # Precargar en CPU
)

# 2. Cargar adaptadores LoRA
model = PeftModel.from_pretrained(base_model, "models/lora")

# 3. Configurar generación - ¡SIN parámetro device!
generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    # device="cpu",  # ← Eliminar esta línea
    do_sample=True,
    temperature=0.7,
    max_length=200,
    truncation=True
)

# 4. Generar respuesta
prompt = "¿Es ético el aborto desde la ética del cuidado? Respuesta:"
result = generator(prompt)

print(result[0]['generated_text'])