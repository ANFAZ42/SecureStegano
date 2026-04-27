from flask import Flask, request, send_file, jsonify
import os
import sys
import webbrowser
from threading import Timer, Thread
import uuid

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from src.steganography import SteganographyEngine
from src.analysis import detect_steganography_lsb

app = Flask(__name__)

JOBS = {}  # Store job state tracking

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/progress/<job_id>', methods=['GET'])
def get_progress(job_id):
    if job_id not in JOBS:
        return jsonify({'error': 'Job not found'}), 404
    return jsonify(JOBS[job_id])

@app.route('/download/<job_id>', methods=['GET'])
def download(job_id):
    if job_id not in JOBS or JOBS[job_id].get('status') != 'completed':
        return jsonify({'error': 'Invalid job or not completed'}), 400
    
    if 'output_path' in JOBS[job_id]:
        return send_file(JOBS[job_id]['output_path'], as_attachment=True)
    return jsonify({'error': 'No output available'}), 404

def run_encode_job(job_id, temp_in, password, message, output_path):
    def progress_cb(pct):
        JOBS[job_id]['progress'] = pct
        
    try:
        SteganographyEngine.encode(temp_in, password, message, output_path, progress_callback=progress_cb)
        JOBS[job_id]['status'] = 'completed'
        JOBS[job_id]['output_path'] = output_path
        JOBS[job_id]['progress'] = 100
    except Exception as e:
        JOBS[job_id]['status'] = 'error'
        JOBS[job_id]['error'] = str(e)

@app.route('/encode', methods=['POST'])
def encode():
    if 'image' not in request.files or 'message' not in request.form or 'password' not in request.form:
        return jsonify({'error': 'Missing parameters'}), 400
        
    img_file = request.files['image']
    message = request.form['message']
    password = request.form['password']
    
    os.makedirs('data/temp', exist_ok=True)
    temp_in = os.path.join('data/temp', img_file.filename)
    img_file.save(temp_in)
    
    base_name = os.path.basename(temp_in)
    name, ext = os.path.splitext(base_name)
    output_filename = f"{name}_stego.png"
    output_path = os.path.join('data/output_images', output_filename)
    os.makedirs('data/output_images', exist_ok=True)
    
    job_id = str(uuid.uuid4())
    JOBS[job_id] = {'status': 'running', 'progress': 0, 'type': 'encode'}
    
    thread = Thread(target=run_encode_job, args=(job_id, temp_in, password, message, output_path))
    thread.daemon = True
    thread.start()
    
    return jsonify({'job_id': job_id})

def run_decode_job(job_id, temp_in, password):
    def progress_cb(pct):
        JOBS[job_id]['progress'] = pct
        
    try:
        decoded_message = SteganographyEngine.decode(temp_in, password, progress_callback=progress_cb)
        JOBS[job_id]['status'] = 'completed'
        JOBS[job_id]['message'] = decoded_message
        JOBS[job_id]['progress'] = 100
    except Exception as e:
        JOBS[job_id]['status'] = 'error'
        JOBS[job_id]['error'] = str(e)

@app.route('/decode', methods=['POST'])
def decode():
    if 'image' not in request.files or 'password' not in request.form:
        return jsonify({'error': 'Missing parameters'}), 400
        
    img_file = request.files['image']
    password = request.form['password']
    
    os.makedirs('data/temp', exist_ok=True)
    temp_in = os.path.join('data/temp', img_file.filename)
    img_file.save(temp_in)
    
    job_id = str(uuid.uuid4())
    JOBS[job_id] = {'status': 'running', 'progress': 0, 'type': 'decode'}
    
    thread = Thread(target=run_decode_job, args=(job_id, temp_in, password))
    thread.daemon = True
    thread.start()
    
    return jsonify({'job_id': job_id})

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': 'Missing parameters'}), 400
        
    img_file = request.files['image']
    
    os.makedirs('data/temp', exist_ok=True)
    temp_in = os.path.join('data/temp', img_file.filename)
    img_file.save(temp_in)
    
    try:
        prob = detect_steganography_lsb(temp_in)
        return jsonify({'probability': prob})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(port=5000, debug=False)
