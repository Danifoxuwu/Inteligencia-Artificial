from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    pipeline
)
from peft import PeftModel, PeftConfig
import torch

def main():
    # 1. Cargar configuración PEFT
    peft_config = PeftConfig.from_pretrained("models/lora")
    
    # 2. Cargar modelo base SIN device_map
    base_model = AutoModelForCausalLM.from_pretrained(
        peft_config.base_model_name_or_path,
        torch_dtype=torch.float32,
        low_cpu_mem_usage=True
    )
    
    # 3. Cargar tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        peft_config.base_model_name_or_path
    )
    tokenizer.pad_token = tokenizer.eos_token
    
    # 4. Cargar adaptadores LoRA
    model = PeftModel.from_pretrained(
        base_model,
        "models/lora"
    )
    model.eval()
    
    # 5. Mover todo a CPU explícitamente
    model = model.to('cpu')
    
    # 6. Configurar pipeline SIN parámetro device
    generator = pipeline(
        task="text-generation",
        model=model,
        tokenizer=tokenizer,
        do_sample=True,
        temperature=0.7,
        max_new_tokens=100,
        truncation=True
    )
    
    # 7. Interfaz de chat
    print("Sistema listo (escribe 'salir' para terminar):")
    while True:
        try:
            user_input = input("\nTú: ")
            if user_input.lower() == 'salir':
                break
                
            response = generator(
                f"P: {user_input} R:",
                max_length=150
            )
            print(f"\nIA: {response[0]['generated_text'].split('R:')[-1].strip()}")
            
        except Exception as e:
            print(f"\nError: {str(e)}")
            break

if __name__ == "__main__":
    main()