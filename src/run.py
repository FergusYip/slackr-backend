from slackr import APP, socketio

if __name__ == "__main__":
    socketio.run(APP, debug=True, port=8080)