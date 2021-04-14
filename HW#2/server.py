from flask import Flask, request, render_template, redirect, url_for
import random
app = Flask(__name__)

messages = []
bot_messages = ['hello', 'how are you?', 'I\'m fine', 'bye']

class Message:
  def __init__(self, message, author):
    self.message = message
    self.author = author

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/chat', methods=["GET", "POST"])
def chat():
    if request.method == "GET":
        return render_template('chat.html', messages=messages)
    else:
        message = request.form.get("message")
        my_message = Message(message, 'me')
        robot_message = Message(random.choice(bot_messages), 'robot')
        messages.append(my_message)
        messages.append(robot_message)
        return redirect(url_for('chat'))

@app.route('/static/<path:path>')
def index2(path):
    return app.send_static_file(path)

@app.route('/<path:path>')
def index3(path):
    return app.send_static_file(path)

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
