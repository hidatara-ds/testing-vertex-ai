from flask import Flask, request, jsonify, render_template
import google.auth
import google.generativeai as genai

app = Flask(__name__)

# Set project ID manually
project_id = "your project id in GCP"

# Set up authentication using default credentials
credentials, _ = google.auth.default(
    scopes=['https://www.googleapis.com/auth/cloud-platform']
)

# Configure the Gemini API
genai.configure(
    api_key=None,  # Not needed when using default credentials
    credentials=credentials
)

# Function to call Gemini model
def call_gemini(prompt):
    try:
        # Initialize the Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Generate content
        response = model.generate_content(prompt)
        
        # Return the response text
        return response.text
    except Exception as e:
        print(f"Error calling Gemini: {str(e)}")
        return f"Sorry, I encountered an error: {str(e)}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        
        if not user_message:
            return jsonify({"response": "Please provide a message"}), 400
            
        response = call_gemini(user_message)
        return jsonify({"response": response})
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({"response": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
