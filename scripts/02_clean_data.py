import pandas as pd
import os

def clean_dataset_properly():
    print("🧹 Cleaning Elsa dataset (keeping creative variations)...")
    
    # Load your CSV
    input_path = "./data/elsa_dataset.csv"
    output_path = "./data/elsa_dataset_cleaned.csv"
    
    df = pd.read_csv(input_path)
    print(f"📊 Original dataset: {len(df)} rows")
    
    # Remove only EXACT duplicates (same question AND same answer)
    initial_count = len(df)
    df = df.drop_duplicates()
    exact_duplicates_removed = initial_count - len(df)
    
    print(f"🗑️  Removed {exact_duplicates_removed} exact duplicates")
    print(f"✅ Remaining dataset: {len(df)} rows")
    
    # Show question distribution
    question_counts = df['Question'].value_counts()
    print(f"\n📋 Question distribution:")
    for question, count in question_counts.items():
        print(f"   '{question}': {count} variations")
    
    # Save cleaned data (keeping all creative variations!)
    df.to_csv(output_path, index=False)
    print(f"💾 Saved {len(df)} creative responses to: {output_path}")
    print("🎉 Perfect! This variety will make Elsa more creative!")

if __name__ == "__main__":
    clean_dataset_properly()