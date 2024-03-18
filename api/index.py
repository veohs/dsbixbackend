from flask import Flask, jsonify, request
from dsbix import DSBApi

app = Flask(__name__)

@app.route('/fetch_entries', methods=['GET'])
def fetch_entries_by_day():
    username = 'YOUR_USER'
    password = 'YOUR_PASSWORD'
    klasse = request.args.get('klasse')  # Get 'klasse' from query string
    wanted_day = request.args.get('day')  # Get 'day' from query string

    # Validate the day input
    days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
    if wanted_day.capitalize() not in days:
        return "Ungültiger Tag. Bitte geben Sie einen gültigen Tag ein."

    dsb_client = DSBApi(username, password)
    entries = dsb_client.fetch_entries()

    final = []
    for s in range(len(entries)):
        for i in range(len(entries[s])):
            if entries[s][i]["class"] == klasse and entries[s][i]["day"] == wanted_day.capitalize():
                lesson = entries[s][i]["lesson"]
                subject = entries[s][i]["new_subject"]
                teacher = entries[s][i]["room"]
                oldsubject = entries[s][i]["subject"]
                room = entries[s][i]["new_teacher"]
                vertreter = entries[s][i]["type"]
                text = entries[s][i]["text"]
                final.append({"lesson": lesson, "new_subject": subject, "room": room,
                              "old_subject": oldsubject, "teacher": teacher, "type": vertreter,
                              "text": text})

    message = f"Am {wanted_day.capitalize()} gibt es {str(len(final))} Einträge. "
    for s in final:
        message += f"In der {s['lesson']}. Stunde hast du {s['teacher']} mit {s['room']} in {s['old_subject']}. Grund dafür ist {s['text']}. "
    return jsonify({"message": message})

if __name__ == '__main__':
    app.run()
