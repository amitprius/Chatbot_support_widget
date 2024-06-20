from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Configure the upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.json
    user_message = data['message']
    
    # Here you can process the user message and generate a bot response
    bot_response = f"You said: {user_message}"
    
    return jsonify({'message': bot_response})

@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    
    if file and file.filename.endswith('.pdf'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        return jsonify({'message': 'PDF uploaded successfully', 'file_path': file_path}), 200
    else:
        return jsonify({'message': 'Invalid file format, only PDF files are allowed'}), 400

if __name__ == '__main__':
    app.run(debug=True)
