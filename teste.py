from flask import Flask, make_response

app = Flask(__name__)

print(f"Using Flask version: {Flask.__version__}")

@app.route('/')
def hello():
    data = b"Hello, World!"
    response = make_response(data, content_type='text/plain')
    return response

if __name__ == '__main__':
    app.run(debug=True)