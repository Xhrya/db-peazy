import json
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from flask_restx import Api, Resource
import uuid
from services import upload_file_to_bucket, save_wav_file, add_memory_to_table, get_random_rows, get_k_closest_memories, get_memory, get_audio_file
from speech_to_text import speech_recognize_continuous_from_file
from datetime import datetime
import base64
import os
import logging


BUCKET_NAME = 'audio-file-dbpeazy'

app = Flask(__name__, static_folder='../frontend/build/', static_url_path='/')
CORS(app)
api = Api(app, version='1.0', title='My API', description='A simple Flask-RESTX API', doc='/api/docs/')

# Namespace
ns = api.namespace('hello', description='Hello World operations')
api.add_namespace(ns)

# Endpoint
post_parser = ns.parser()
post_parser.add_argument('audio file', location='files', type='file', required=True, help='WAV audio file')

get_parser = ns.parser()
get_parser.add_argument('maxResults', type=int, help="Maximum number of memories to return")

similarity_get_parser = ns.parser()
similarity_get_parser.add_argument('transcript', type=str, location='form')

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@ns.route('/memory')
class Memory(Resource):
    @ns.expect(post_parser)
    def post(self):
        id = int(uuid.uuid4().int ** (1/5))
        file = request.files['audio file']
        if file.filename.endswith('.wav'):
            save_wav_file(file, 'temp_files/temp_file.wav')
            file.seek(0)
            upload_file_to_bucket(file, BUCKET_NAME, id)
            transcript = speech_recognize_continuous_from_file(filepath='temp_files/temp_file.wav').replace(':', '')
            if transcript == '':
                transcript = ' '
            add_memory_to_table(transcript, datetime.now().isoformat(), id)
            return 200
        return "Incorrect file format. Upload a .wav file.", 400

    @ns.expect(get_parser)
    def get(self):
        max_results = request.args.get('maxResults')
        if not max_results:
            max_results = 10
        response = {
            "memories": get_random_rows(max_results)
        }

        return json.dumps(response)


@ns.route('/memory/<int:id>')
class SingleMemory(Resource):
    def get(self, id):
        memory = get_memory(id)[0]
        related_memories = [m.metadata for m in get_k_closest_memories(memory['transcript'], 3)]
        memory['related_memories'] = related_memories
        response = {
            "memory": memory
        }
        return json.dumps(response)

@ns.route('/memory/audio/<int:id>')
class Audio(Resource):
    def get(self, id):
        get_audio_file(id)
        with open('temp_files/temp_download.wav', 'rb') as file:
            file_bytes = file.read()

        base64_string = base64.b64encode(file_bytes).decode('utf-8')

        response = {
            "audio_file_base64": base64_string
        }

        return json.dumps(response)

@ns.route('/memory/similarity')
class Similarity(Resource):
    @ns.expect(similarity_get_parser)
    def post(self):
        transcript = request.form['transcript']
        memories = [m.metadata for m in get_k_closest_memories(transcript, 3)]
        response = {
            "memories": memories
        }
        return json.dumps(response)

@app.route('/memories', methods=['GET'])
@app.route('/', methods=['GET'])
def serve_index():
    for root, dirs, files in os.walk("../"):
        for file in files:
            # Construct the full file path
            file_path = os.path.join(root, file)
            logger.debug(file_path)
    return send_from_directory(app.static_folder, 'index.html')

@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
