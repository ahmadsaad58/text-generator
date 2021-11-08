from app import app

if __name__ == "__main__":
    try:
        # run regularly
        app.run(host="0.0.0.0", port=80, threaded=True, debug=True)
    except:
        # autoswitch port
        app.run(host="0.0.0.0", port=90, threaded=True, debug=True)
