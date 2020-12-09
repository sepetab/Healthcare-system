from routes import app


if __name__ == '__main__':
    # SIGINT to stop (Ctrl + C)
    app.run(debug=True, port = 5003, use_reloader=True)
