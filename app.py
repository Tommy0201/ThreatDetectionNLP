from flask import Flask
from threat_keywords import find_threatening_token
from threat_detection import threaten_detection
from flask import Flask, request, jsonify

app = Flask(__name__)

context = ""
conversation = ""
@app.route('/')
def hello_world():
    return "Hello, World!"


@app.route('/delete',methods=['POST'])
def delete_conversation():
    global context
    context = ""  
    return jsonify({"message": "Conversation deleted successfully"})

@app.route('/chat-history', methods=['POST'])
def fetch_history():
    global conversation
    return jsonify({"conversation": conversation})


@app.route('/detect', methods=['POST'])
def detect_threat():

    global context
    global conversation
    data = request.json
    conversation = conversation + "/n" + data
    
    if find_threatening_token(data):
        threaten = "yes"
    else:
        out = threaten_detection(context, data)
        new_context, threaten = out.get('summary',''), out.get('threaten','')
        if context:
            context += new_context
        else: 
            context = new_context
            
    out = {"answer": threaten, "context": context,"conversation":conversation}
    
    print(out)
    return jsonify(out)

if __name__ == '__main__':
    app.run(port=5000)
