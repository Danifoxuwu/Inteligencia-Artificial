from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model
from datasets import load_dataset
import torch

# 1. Configuración del modelo
model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token  # Importante para evitar errores

# 2. Cargar y preparar el dataset
dataset = load_dataset("json", data_files="data/dataset.jsonl", split="train")

def preprocess_function(examples):
    return tokenizer(examples["text"], truncation=True, max_length=512)

tokenized_dataset = dataset.map(
    preprocess_function,
    batched=True,
    remove_columns=["text"]  # Elimina la columna original
)

# 3. Configurar el modelo
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="cpu",
    torch_dtype=torch.float32
)

# 4. Configuración LoRA
peft_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "k_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, peft_config)

# 5. Configuración del entrenamiento
training_args = TrainingArguments(
    output_dir="./results",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    num_train_epochs=1,
    save_steps=100,
    logging_steps=10,
    learning_rate=2e-5,
    fp16=False,
    remove_unused_columns=False,  # ¡IMPORTANTE!
    optim="adamw_torch"
)

# 6. Data Collator para lenguaje
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False
)

# 7. Configurar Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    data_collator=data_collator
)

# 8. Entrenar
trainer.train()
model.save_pretrained("models/lora")