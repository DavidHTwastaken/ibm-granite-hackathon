import os
import json
import shutil
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
import subprocess
from project import ProjectCompiler
import tempfile
import zipfile
if os.environ.get('DRY') == None:
    from models.doc import generate_doc
    from models.audio import audio_to_text
app = Flask(__name__)
CORS(app)

# where we'll store uploads
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'AudioUploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# where we'll store uploaded zip files
ZIP_DIR = os.path.join(os.path.dirname(__file__), 'zipped-Code')
os.makedirs(ZIP_DIR, exist_ok=True)

# transcript file path
TRANSCRIPT_PATH = os.path.join(os.path.dirname(__file__), 'transcript.json')

# allowed extensions
ALLOWED_AUDIO_EXT = {'wav'}
ALLOWED_ZIP_EXT = {'zip'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max

# Helper function to clear directories
def clear_directory(directory):
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Remove file or symlink
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Remove directory
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")

# Clear directories on server startup
clear_directory(UPLOAD_FOLDER)
clear_directory(ZIP_DIR)

# transcript helpers
def load_transcript():
    if not os.path.exists(TRANSCRIPT_PATH):
        with open(TRANSCRIPT_PATH, 'w') as f:
            json.dump({"transcript": ""}, f)
    with open(TRANSCRIPT_PATH, 'r') as f:
        return json.load(f)

def save_transcript(data):
    with open(TRANSCRIPT_PATH, 'w') as f:
        json.dump(data, f, indent=2)

# file-check helpers
def allowed_audio_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_AUDIO_EXT

def allowed_zip_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_ZIP_EXT

@app.route('/')
def root():
    return 'Nothing to see here folks, move along!'

@app.route('/test', methods=['GET'])
def test():
    # sample data
    return jsonify([
      {"_id": "6812eb7ab5c84bd4c4d5d414", "name": "Fernandez Franklin", "gender": "male", "company": "STOCKPOST"},
      {"_id": "6812eb7ab5ba613bbbfe4957", "name": "Lora Middleton", "gender": "female", "company": "PAPRICUT"},
      {"_id": "6812eb7aa902215c8436245a", "name": "Jennings Blankenship", "gender": "male", "company": "EQUICOM"},
      {"_id": "6812eb7a83f5f49c410d74a2", "name": "Kelley Frederick", "gender": "female", "company": "KNOWLYSIS"},
      {"_id": "6812eb7a51dde1459e1061af", "name": "Angelique Peterson", "gender": "female", "company": "SEALOUD"},
      {"_id": "6812eb7a7bc7d0b35655e5ca", "name": "Dejesus Austin", "gender": "male", "company": "GOGOL"},
      {"_id": "6812eb7ade2830023da19148", "name": "Therese Perez", "gender": "female", "company": "QABOOS"}
    ])

@app.route('/transcript', methods=['GET', 'POST'])
def transcript():
    if request.method == 'GET':
        data = load_transcript()
        return jsonify(data)

    # POST: update transcript
    payload = request.get_json()
    if not payload or 'transcript' not in payload:
        return jsonify(error="Missing 'transcript' field"), 400

    new_text = payload['transcript']
    save_transcript({"transcript": new_text})
    return jsonify(success=True), 200

@app.route('/audio-input', methods=['POST', 'OPTIONS'])
def audio_input():
    if request.method == 'OPTIONS':
        return '', 200

    if 'file' not in request.files:
        return jsonify(error="No file part in request"), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify(error="No selected file"), 400

    if not allowed_audio_file(file.filename):
        return jsonify(error="File type not allowed"), 400

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False, dir=app.config['UPLOAD_FOLDER']) as temp_audio:
        audio_path = temp_audio.name
        file.save(audio_path)
    tmp_save_path = os.path.join(audio_path)
    save_path = os.path.join(audio_path.replace('.wav', '_converted.wav'))

    # Convert audio to desired format
    result = subprocess.run([
        "ffmpeg",
        "-i", tmp_save_path,
        "-ar", "16000",
        "-ac", "1",
        "-c:a", "pcm_s16le",
        '-sample_fmt', 's16',
        save_path
    ], capture_output=True, text=True)
    os.remove(tmp_save_path)
    # process audio
    transcript = audio_to_text(save_path)
    os.remove(save_path)
    return jsonify(success=True, transcript=transcript), 200

@app.route('/zip-file', methods=['POST'])
def zip_file():
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify(error="No selected file"), 400

    if not allowed_zip_file(file.filename):
        return jsonify(error="Only .zip files allowed"), 400

    filename = secure_filename(file.filename)
    save_path = os.path.join(ZIP_DIR, filename)
    file.save(save_path)

    return jsonify(success=True, filename=filename), 200

@app.route('/generate', methods=['POST'])
def generate():
    # process zip file
    if 'zipFile' not in request.files:
        return jsonify(error="No zip file part"), 400

    project = request.files['zipFile']
    if project.filename == '':
        return jsonify(error="No selected file"), 400

    if not allowed_zip_file(project.filename):
        return jsonify(error="Only .zip files allowed"), 400

    with tempfile.NamedTemporaryFile(suffix=".zip", delete=False, dir=ZIP_DIR) as temp_zip:
        zip_path = temp_zip.name
        project.save(zip_path)
    
    with tempfile.TemporaryDirectory(dir=ZIP_DIR, delete=False) as temp_dir:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        os.remove(zip_path)

    # Compile the project files into a single text file
    output_file = os.path.join(temp_dir, 'compiled_project.txt')
    pc = ProjectCompiler(temp_dir)
    pc.project_to_txt(output_file, verbose=True)
    
    # zip_filename = secure_filename(project.filename)
    # save_path = os.path.join(ZIP_DIR, zip_filename)
    # project.save(save_path)

    # process transcript
    if 'transcript' not in request.form:
        return jsonify(error="No transcript part"), 400

    project = request.form['transcript']
    
    # run the generate_doc function
    doc = generate_doc(project, description=output_file)
    return jsonify(output=doc), 200
  
  
if __name__ == '__main__':
    app.run(debug=True)
