# import sys
# sys.path.append('..')

# from transformers import (
#     AutoModelForCausalLM, 
#     AutoTokenizer
# )
# from peft import PeftModel
# import torch
# import re

# def clean_response(text):
#     """Clean up the model's response"""
#     # Remove all <|...|> tags and special characters
#     text = re.sub(r'<\|[^>]*\|>', '', text)
#     text = re.sub(r'[\*\^\{\}\|\\\$\@\<\>]', '', text)
#     text = re.sub(r'\s+', ' ', text).strip()
    
#     # Remove everything after strange artifacts
#     text = text.split('</s>')[0]
#     text = text.split('Another cold day')[0]
#     text = text.split('The following generation')[0]
    
#     if text and len(text) > 0:
#         text = text[0].upper() + text[1:]
    
#     return text

# def chat_with_elsa_final():
#     print("❄️" * 40)
#     print("   ELSA AI CHATBOT - Final Version!")
#     print("❄️" * 40)
#     print("Type 'quit' to exit")
#     print("Type 'reset' to clear conversation history")
#     print("-" * 40)
    
#     print("🧊 Loading Elsa...")
    
#     # Load base model
#     model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    
#     model = AutoModelForCausalLM.from_pretrained(
#         model_name,
#         device_map="auto",
#         torch_dtype=torch.float16,
#     )
    
#     # Load our fine-tuned adapter
#     model = PeftModel.from_pretrained(model, "./trained_model")
#     tokenizer = AutoTokenizer.from_pretrained("./trained_model")
    
#     if tokenizer.pad_token is None:
#         tokenizer.pad_token = tokenizer.eos_token
    
#     model.eval()
    
#     print("✅ Elsa is ready! Start chatting...")
#     print("-" * 40)
    
#     while True:
#         user_input = input("\nYou: ").strip()
        
#         if user_input.lower() == 'quit':
#             print("Elsa: Goodbye! The cold never bothered me anyway... ❄️")
#             break
            
#         if user_input.lower() == 'reset':
#             print("Conversation history cleared!")
#             continue
            
#         # Simple prompt format that works
#         prompt = f"User: {user_input}\nElsa: "
        
#         # Tokenize
#         inputs = tokenizer(
#             prompt, 
#             return_tensors="pt", 
#             truncation=True, 
#             max_length=256
#         )
        
#         print("Elsa: ", end="", flush=True)
        
#         with torch.no_grad():
#             outputs = model.generate(
#                 **inputs,
#                 max_new_tokens=80,
#                 temperature=0.8,
#                 do_sample=True,
#                 pad_token_id=tokenizer.eos_token_id,
#                 repetition_penalty=1.1,
#                 no_repeat_ngram_size=2,
#             )
        
#         # Decode response
#         full_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
#         # Extract response
#         if "Elsa: " in full_response:
#             elsa_response = full_response.split("Elsa: ")[-1].strip()
#         else:
#             elsa_response = full_response.replace(prompt, "").strip()
        
#         # Clean up
#         elsa_response = clean_response(elsa_response)
        
#         # Ensure we have a response
#         if not elsa_response or len(elsa_response) < 3:
#             elsa_response = "I'm still learning to express myself clearly. Could you ask me something else?"
        
#         print(elsa_response)

# if __name__ == "__main__":
#     chat_with_elsa_final()


import sys
sys.path.append('..')

from transformers import (
    AutoModelForCausalLM, 
    AutoTokenizer
)
from peft import PeftModel
import torch
import re

def clean_response(text):
    """Clean up the model's response and handle cut-off sentences"""
    # Remove all <|...|> tags and special characters
    text = re.sub(r'<\|[^>]*\|>', '', text)
    text = re.sub(r'[\*\^\{\}\|\\\$\@\<\>]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove everything after strange artifacts or newlines
    text = text.split('\n')[0]
    text = text.split('</s>')[0]
    text = text.split('Another cold day')[0]
    text = text.split('The following generation')[0]
    
    # Remove any remaining "Elsa: " prefixes
    text = re.sub(r'^(Elsa|AI|Assistant):\s*', '', text)
    
    # Handle cut-off sentences
    if text and not text.endswith(('.', '!', '?', '"', "'")):
        # If the sentence was cut off, try to find a logical breaking point
        last_period = text.rfind('.')
        last_exclamation = text.rfind('!')
        last_question = text.rfind('?')
        
        # Find the last proper sentence ending
        last_ending = max(last_period, last_exclamation, last_question)
        
        if last_ending > 0 and len(text) - last_ending < 20:  # If we have a recent ending
            text = text[:last_ending + 1]  # Keep up to the sentence end
        else:
            # Just remove the last incomplete word
            text = text.rsplit(' ', 1)[0] 
            if text and not text.endswith(('.', '!', '?')):
                text += '.'  # Add a period to complete it
    
    if text and len(text) > 0:
        text = text[0].upper() + text[1:]
    
    return text

def get_max_tokens_for_question(user_input, current_mode):
    """
    Determine max_new_tokens based on both the user's question
    and the current response length mode.
    """
    # If manual mode is active, respect it above all else
    if current_mode == 'long':
        return 180  # Increased to allow completion
    elif current_mode == 'short':
        return 65   # Increased to allow completion
    
    # Otherwise, use keyword-based dynamic adjustment
    user_input_lower = user_input.lower()
    
    # Keywords that typically require longer answers
    long_answer_keywords = [
        'explain', 'tell me about', 'story', 'what happened', 
        'how did', 'why did', 'describe', 'remember when',
        'elaborate', 'what do you think about', 'how do you feel about'
    ]
    
    # Check for explanatory questions
    for keyword in long_answer_keywords:
        if keyword in user_input_lower:
            return 140  # Longer response for explanatory questions
    
    # Default token limit for simple chats
    return 85

def chat_with_elsa_final():
    print("❄️" * 40)
    print("   ELSA AI CHATBOT - Dynamic Length Version!")
    print("❄️" * 40)
    print("Type 'quit' to exit")
    print("Type 'reset' to clear conversation history")
    print("Use '/long' or '/short' to manually control response length")
    print("Type '/auto' to return to automatic mode")
    print("-" * 40)
    
    print("🧊 Loading Elsa...")
    
    # Load base model
    model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto",
        torch_dtype=torch.float16,
    )
    
    # Load our fine-tuned adapter
    model = PeftModel.from_pretrained(model, "./trained_model")
    tokenizer = AutoTokenizer.from_pretrained("./trained_model")
    
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    model.eval()
    
    print("✅ Elsa is ready! Start chatting...")
    print("-" * 40)
    
    # Response mode state: 'auto', 'long', or 'short'
    response_mode = 'auto'
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'quit':
            print("Elsa: Goodbye! The cold never bothered me anyway... ❄️")
            break
            
        if user_input.lower() == 'reset':
            print("Conversation history cleared!")
            response_mode = 'auto'  # Reset mode too
            continue
        
        # Check for mode change commands
        original_input = user_input
        if user_input.lower() == '/long':
            response_mode = 'long'
            print("(Response mode set to LONG)")
            continue
        elif user_input.lower() == '/short':
            response_mode = 'short'
            print("(Response mode set to SHORT)")
            continue
        elif user_input.lower() == '/auto':
            response_mode = 'auto'
            print("(Response mode set to AUTO)")
            continue
        elif user_input.startswith('/long '):
            response_mode = 'long'
            user_input = user_input[6:]  # Remove the '/long ' part
            print("(Long response for this question)")
        elif user_input.startswith('/short '):
            response_mode = 'short'
            user_input = user_input[7:]  # Remove the '/short ' part
            print("(Short response for this question)")
        
        # If input is empty after command processing, skip
        if not user_input:
            continue
            
        # Get the appropriate token limit
        max_tokens = get_max_tokens_for_question(user_input, response_mode)
        
        # Display mode info if not in auto mode
        mode_info = ""
        if response_mode != 'auto':
            mode_info = f" [{response_mode.upper()} mode: {max_tokens}tokens]"
        
        # Use the structured prompt format
        system_prompt = """You are Elsa, the Snow Queen from Arendelle. You are kind, magical, and speak in a warm but regal tone. You are having a casual conversation. Respond directly to what the user says."""
        
        prompt = f"<|system|>\n{system_prompt}</s>\n<|user|>\n{user_input}</s>\n<|assistant|>\nElsa: "
        
        # Tokenize
        inputs = tokenizer(
            prompt, 
            return_tensors="pt", 
            truncation=True, 
            max_length=512
        )
        
        print(f"Elsa{mode_info}: ", end="", flush=True)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=0.7,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
                repetition_penalty=1.2,
                eos_token_id=tokenizer.eos_token_id,
                # REMOVED: early_stopping and length_penalty (incompatible with sampling)
                # ADDED: top_p for better sampling control
                top_p=0.9,
            )
        
        # Decode response
        full_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract only the part after the last "Elsa: "
        if "Elsa: " in full_response:
            elsa_response = full_response.split("Elsa: ")[-1].strip()
        else:
            elsa_response = full_response.replace(prompt, "").strip()
        
        # Clean up and handle cut-off sentences
        elsa_response = clean_response(elsa_response)
        
        # Ensure we have a response
        if not elsa_response or len(elsa_response) < 2:
            elsa_response = "It's so good to see you."
        
        print(elsa_response)
        
        # If we used a one-time command (/long question), revert to auto mode
        if original_input.startswith(('/long ', '/short ')):
            response_mode = 'auto'

if __name__ == "__main__":
    chat_with_elsa_final()