from flask import Flask, render_template, Response, send_from_directory, url_for, request
from flask_socketio import SocketIO, emit
import settings.settings as settings

app = Flask(__name__)
socketio = SocketIO(app, async_handlers=True)

@socketio.on('registration_request')
def return_registration(stream_id):
    print("received registration request")
    #port = settings.next_available_port()
    with open('settings/client_list.txt', 'a') as f:
        f.write(str(stream_id))
    emit("registration_ack", { 'data' : 'thanks!' } )


def run_registration_server():
    #run the server
    print("booting registration server")
    socketio.run(app, host='0.0.0.0', debug=False, port=8001)
