from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/hello')
def hello():
    return jsonify(message="Hello, world!")

@app.route('/users')
def users():
    sample = [ {"id":1,"name":"Alice"}, {"id":2,"name":"Bob"} ]
    return jsonify(users=sample)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
