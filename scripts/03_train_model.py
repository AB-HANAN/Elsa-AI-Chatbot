import sys
sys.path.append('..')

from transformers import (
    AutoModelForCausalLM, 
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from datasets import Dataset
import pandas as pd
import torch
from peft import LoraConfig, get_peft_model, TaskType
import os

def train_elsa_model():
    print("🚀 Starting Elsa AI Training (Standard Version)...")
    print("❄️" * 40)
    
    # 1. Load CLEANED Dataset
    print("📖 Loading cleaned dataset...")
    df = pd.read_csv("./data/elsa_dataset_cleaned.csv")
    dataset = Dataset.from_pandas(df)
    print(f"✅ Loaded {len(dataset)} training examples")
    
    # 2. Load Base Model (TinyLlama) - WITHOUT unsloth
    print("🧠 Loading TinyLlama model...")
    model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        load_in_4bit=True,
        device_map="auto",
        torch_dtype=torch.float16,
    )
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token
    
    # 3. Prepare Model for LoRA Training
    print("⚙️ Preparing model for LoRA training...")
    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                       "gate_proj", "up_proj", "down_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.CAUSAL_LM
    )
    
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    
    # 4. Format Training Data
    print("📝 Formatting training data...")
    def format_chat_template(row):
        question = row["Question"]
        answer = row["Answer"]
        text = f"<|user|>\n{question}<|end|>\n<|assistant|>\n{answer}<|end|>"
        return {"text": text}
    
    def tokenize_function(examples):
        # Tokenize the text
        tokenized = tokenizer(
            examples["text"],
            truncation=True,
            padding=False,
            max_length=512,
            return_tensors=None
        )
        return tokenized
    
    dataset = dataset.map(format_chat_template)
    tokenized_dataset = dataset.map(tokenize_function, batched=True)
    
    # 5. Set Up Training
    print("⚡ Setting up training configuration...")
    training_args = TrainingArguments(
        output_dir="../output",
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        warmup_steps=10,
        num_train_epochs=2,  # Reduced for CPU training
        learning_rate=2e-4,
        fp16=False,  # Disable FP16 for CPU
        logging_steps=1,
        save_strategy="no",
        report_to=None,
        optim="adamw_torch",
    )
    
    # Create data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
    )
    
    # Create trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        data_collator=data_collator,
    )
    
    # 6. Start Training!
    print("🔥 Starting training... This will take several hours...")
    print("⏰ Go take a break, watch a movie, the model is learning!")
    print("❄️" * 40)
    
    trainer.train()
    
    # 7. Save the Model
    print("💾 Saving trained model...")
    model.save_pretrained("./trained_model")
    tokenizer.save_pretrained("./trained_model")
    
    print("🎉 Training complete! Model saved to 'trained_model/' folder")
    print("You can now run '04_chat_with_elsa_no_unsloth.py' to talk to Elsa!")

if __name__ == "__main__":
    train_elsa_model()