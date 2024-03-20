from flask import Flask, jsonify, request
from dsbix import DSBApi
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Erlaubt CORS für alle Endpunkte der Flask-Anwendung

# Defining DSB client globally
dsbclient = DSBApi("299761", "cicero2223", tablemapper=['class', 'lesson', 'new_subject', 'room', 'subject', 'new_teacher', 'type', 'text', 'update'])

@app.route('/fetch_entries', methods=['GET'])
def fetch_entries_by_day():
    klasse = request.args.get('klasse')  # Getting class from request parameters
    wanted_day = request.args.get('day')  # Getting day from request parameters
    
    days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
    if wanted_day.capitalize() not in days:
        return jsonify({"error": "Ungültiger Tag. Bitte geben Sie einen gültigen Tag ein."}), 400

    entries = dsbclient.fetch_entries()
    
    final = []

    for s in range(len(entries)):
        for i in range(len(entries[s])):
            if entries[s][i]["class"] == klasse:
                if entries[s][i]["day"] == wanted_day.capitalize():
                    lesson = entries[s][i]["lesson"]
                    new_subject = entries[s][i]["room"]  # Corrected this line
                    room = entries[s][i]["new_subject"]  # Corrected this line
                    old_subject = entries[s][i]["subject"]
                    teacher = entries[s][i]["new_teacher"]
                    vertreter = entries[s][i]["type"]
                    text = entries[s][i]["text"]
                    
                    final.append({"lesson": lesson, "new_subject": new_subject, "room": old_subject, "teacher": teacher, "type": vertreter, "text": text})

    if not final:
        return jsonify({"message": f"Am {wanted_day.capitalize()} gibt es keine Einträge für die Klasse {klasse}."})

    return jsonify(final)

if __name__ == '__main__':
    app.run()
