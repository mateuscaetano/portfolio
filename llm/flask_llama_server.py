from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
import logging
import keyring as kr
from huggingface_hub import login


# Login to HuggingFace using Token
login(kr.get_password('hf','hf'))


# Load the LLaMA model and tokenizer
llama_pipeline = pipeline(
    "text-generation",
    model="meta-llama/Llama-3.2-1B-Instruct",  # Replace with your LLaMA model
    device_map="auto",  # Automatically map to GPU if available
)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

@app.route("/v1/completions", methods=["POST"])
def completions():
    """
    Handle completion requests similar to OpenAI API structure.
    """
    try:
        # Parse request payload
        data = request.json
        prompt = data.get("prompt", "")
        max_tokens = data.get("max_tokens", 128)
        temperature = data.get("temperature", 0.7)
        top_p = data.get("top_p", 1.0)

        # Generate response using LLaMA
        results = llama_pipeline(
            prompt,
            max_new_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            return_full_text=False,
        )

        print(results)
        # Structure the response to mimic OpenAI's API
        return jsonify({
            "choices": [{
                "text": results[0]["generated_text"]
            }]
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/v1/chat/completions", methods=["POST"])
def chat_completions():
    """
    Handle chat completions requests similar to OpenAI API structure.
    """
    try:
        # Parse request payload
        data = request.json
        messages = data.get("messages", [])
        max_tokens = data.get("max_tokens", 128)
        temperature = data.get("temperature", 0.7)
        top_p = data.get("top_p", 1.0)

        #Combine messages into a singe prompt
        prompt = ""
        for message in messages:
            role = message["role"]
            content = message["content"]
            if role == "user":
                prompt += f"User: {content}\n"
            elif role == "assistant":
                prompt += f"Assistant: {content}\n"

        # Generate response using LLaMA
        results = llama_pipeline(
            prompt,
            max_new_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            return_full_text=False,
            num_return_sequences=1
        )

        print(results)
        # Structure the response to mimic OpenAI's API
        return jsonify({
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": results[0]["generated_text"]
                }
            }]
        }), 200
        
    except Exception as e:
        logging.info(str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


'''Sample request

curl -X POST http://localhost:5000/v1/completions -H "Content-Type: application/json" -d '{"prompt": "Write a short poem about the stars.", "max_tokens": 50}'

'''

