from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch
import re
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Global variables for model and tokenizer
model = None
tokenizer = None
response_mode = 'auto'  # Track response mode globally

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

def load_model():
    """Load the model once when the server starts"""
    global model, tokenizer
    print("🧊 Loading Elsa...")
    
    try:
        # Create offload directory if it doesn't exist
        os.makedirs("./offload", exist_ok=True)
        
        # Load base model with offloading support
        model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            torch_dtype=torch.float16,
            offload_folder="./offload",    # Critical for memory management
            offload_state_dict=True,       # Offload state dict to disk
        )
        
        # Load our fine-tuned adapter with offloading
        model = PeftModel.from_pretrained(
            model, 
            "./trained_model",
            offload_folder="./offload",    # Offload for adapter too
        )
        
        tokenizer = AutoTokenizer.from_pretrained("./trained_model")
        
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        model.eval()
        print("✅ Elsa is ready! (With optimal memory management)")
        print("❄️" * 40)
        
    except Exception as e:
        print(f"❌ Error with GPU loading: {e}")
        print("🔄 Falling back to CPU mode...")
        
        # Fallback to CPU mode - guaranteed to work
        model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="cpu",              # Force CPU mode
            torch_dtype=torch.float32,     # Use float32 for CPU
        )
        
        model = PeftModel.from_pretrained(model, "./trained_model")
        tokenizer = AutoTokenizer.from_pretrained("./trained_model")
        
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        model.eval()
        print("✅ Elsa is ready! (Running on CPU - slower but reliable)")
        print("❄️" * 40)

@app.route('/api/chat', methods=['POST'])
def chat_with_elsa():
    """API endpoint that matches your original chat functionality"""
    global response_mode
    
    try:
        data = request.json
        user_input = data.get('message', '').strip()
        current_mode = data.get('mode', response_mode)  # Allow mode override from client
        
        if not user_input:
            return jsonify({'error': 'No message provided'}), 400
        
        # Handle mode change commands
        original_input = user_input
        if user_input.lower() == '/long':
            response_mode = 'long'
            return jsonify({'response': '(Response mode set to LONG)', 'mode': response_mode})
        elif user_input.lower() == '/short':
            response_mode = 'short'
            return jsonify({'response': '(Response mode set to SHORT)', 'mode': response_mode})
        elif user_input.lower() == '/auto':
            response_mode = 'auto'
            return jsonify({'response': '(Response mode set to AUTO)', 'mode': response_mode})
        elif user_input.startswith('/long '):
            current_mode = 'long'
            user_input = user_input[6:]  # Remove the '/long ' part
        elif user_input.startswith('/short '):
            current_mode = 'short'
            user_input = user_input[7:]  # Remove the '/short ' part
        
        # If input is empty after command processing
        if not user_input:
            return jsonify({'response': 'Please provide a message after the command.', 'mode': response_mode})
        
        # Get the appropriate token limit
        max_tokens = get_max_tokens_for_question(user_input, current_mode)
        
        # Use the structured prompt format from your original code
        system_prompt = """You are Elsa, the Snow Queen from Arendelle. You are kind, magical, and speak in a warm but regal tone. You are having a casual conversation. Respond directly to what the user says."""
        
        prompt = f"<|system|>\n{system_prompt}</s>\n<|user|>\n{user_input}</s>\n<|assistant|>\nElsa: "
        
        # Tokenize
        inputs = tokenizer(
            prompt, 
            return_tensors="pt", 
            truncation=True, 
            max_length=512
        )
        
        # Move inputs to the same device as model
        device = next(model.parameters()).device
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        # Generate response
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=0.7,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
                repetition_penalty=1.2,
                eos_token_id=tokenizer.eos_token_id,
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
        
        # If we used a one-time command, revert to previous mode
        final_mode = response_mode
        if original_input.startswith(('/long ', '/short ')):
            final_mode = 'auto'
        
        return jsonify({
            'response': elsa_response,
            'mode': final_mode,
            'tokens': max_tokens
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Something went wrong with Elsa\'s magic', 'mode': response_mode}), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get current status and mode"""
    device = next(model.parameters()).device if model else 'cpu'
    return jsonify({
        'status': 'Elsa is ready!',
        'mode': response_mode,
        'device': str(device),
        'endpoints': {
            'chat': '/api/chat (POST)',
            'status': '/api/status (GET)'
        }
    })

@app.route('/')
def home():
    device = next(model.parameters()).device if model else 'cpu'
    return f"""
    <h1>Elsa AI Chatbot API</h1>
    <p>❄️ Welcome to Arendelle! Elsa's API is running.</p>
    <p>Running on: <strong>{device}</strong></p>
    <p>Current mode: <strong>{response_mode}</strong></p>
    <p>Use <code>/api/chat</code> endpoint to talk to Elsa.</p>
    """

# Load model when server starts
load_model()

if __name__ == '__main__':
    print("❄️" * 40)
    print("   ELSA AI CHATBOT API - Dynamic Length Version!")
    print("❄️" * 40)
    print("API endpoints:")
    print("  GET  /api/status  - Get current status")
    print("  POST /api/chat    - Chat with Elsa")
    print("  GET  /            - This info page")
    print("-" * 40)
    device = next(model.parameters()).device if model else 'cpu'
    print(f"Running on device: {device}")
    print("🚀 Starting Flask server on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)