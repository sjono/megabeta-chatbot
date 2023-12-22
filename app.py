from flask import Flask, request, jsonify, send_from_directory, redirect, url_for
import json
from answer_questions import answer_question
from answer_questions import answer_questions

app = Flask(__name__)


@app.route('/<path:path>')
def serve_static(path):
  # Serve file from public directory
  return send_from_directory('public', path)


@app.route('/')
def index():
  return send_from_directory('public', 'index.html')


@app.route('/ask', methods=['POST'])
def ask():
  # Get message from request body
  data = json.loads(request.data)
  print("Data: " + str(request.data))
  # Extract transcript and promptType from data
  transcript = data['transcript']
  last_message = transcript[-1]["text"]
  print("Message: " + str(last_message))
  answer = answer_question(last_message)
  #answer, file_names = answer_question(last_message) # updated to receive a tuple
  print("Answer: " + str(answer))
  # print(f"Answer: {answer}\n\nSource Files: {', '.join(file_names)}\n") # print answer + source
  #return f"{answer}\n\nSource Files: {', '.join(file_names)}\n" # Send back answer and source
  return str(answer)


@app.errorhandler(Exception)
def error(e):
  print("error: " + str(e))
  print(request.url)
  return "error! " + str(e)


def run():
  app.run(host='0.0.0.0')
