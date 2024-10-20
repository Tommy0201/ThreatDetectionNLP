from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from threat_keywords import find_threatening_token
from threat_detection import threaten_detection
from summarization import summary
import json

app = Flask(__name__)
socketio = SocketIO(app)
sio = socketio.Server(cors_allowed_origins="*")
CORS(app)


conversation = ""

@app.route('/')
def hello_world():
    return "Hello, World!"

@app.route('/delete', methods=['POST'])
def delete_conversation():
    global conversation
    conversation = ""
    context = ""  
    return jsonify({"conversation": conversation})

@app.route('/history', methods=['POST'])
def history():
    global conversation
    return jsonify({"conversation": conversation})

@app.route('/detect', methods=['POST'])
def detect_threat():
    global conversation
    data = request.json
    transcription = data['transcription']    
    print("transcript: ", type(transcription))
    print("transcription: ",)
    # Convert transcription dict to a string (or keep as needed)
    if isinstance(transcription, dict):
        transcription = json.dumps(transcription)  # Convert dict to a JSON string if needed

    # transcription = data['transcription']
    res, threaten_type = find_threatening_token(transcription)
    if res:
        threaten = "yes"

    else: 
        out = threaten_detection(conversation, transcription)
        # print(type(transcription))
        threaten_type, threaten = out.get('threat_type', 'none'), out.get('threaten', 'no')
    if isinstance(conversation, str):
        conversation += "\n" + transcription
    else:
        conversation = str(conversation) + "\n" + transcription
    conversation = summary(conversation).get('summary','none')
    out = {"answer": threaten, "threaten_type": threaten_type,  "conversation": conversation}
    
    print(out)
    return jsonify(out)

if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', port=4900)
