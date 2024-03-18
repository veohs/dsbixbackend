from flask import Flask, jsonify
from dsbix import DSBApi

app = Flask(__name__)

@app.route('/fetch_entries')
def fetch_entries():
    username = '299761'
    password = 'cicero2223'
    dsb_client = DSBApi(username, password)
    entries = dsb_client.fetch_entries()

    # Filter entries for class "10a"
    class_10a_entries = [entry for entry in entries if entry.get("class") == "10a"]

    return jsonify(class_10a_entries)

if __name__ == '__main__':
    app.run()
