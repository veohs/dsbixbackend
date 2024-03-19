from flask import Flask, jsonify, request
from dsbix import DSBApi

app = Flask(__name__)

# Defining DSB client globally
dsbclient = DSBApi("299761", "cicero2223", tablemapper=['class','lesson','new_subject','room','subject','new_teacher','type','text','update'])

@app.route('/fetch_entries', methods=['GET'])
def fetch_entries_by_day():
    klasse = request.args.get('klasse')  # Getting class from request parameters
    wanted_day = request.args.get('day')  # Getting day from request parameters
    
    days = ["Montag","Dienstag","Mittwoch","Donnerstag","Freitag"]
    if wanted_day.capitalize() not in days:
        return "Ungültiger Tag. Bitte geben Sie einen gültigen Tag ein."

    entries = dsbclient.fetch_entries()
    
    final = []

    for s in range(len(entries)):
        for i in range(len(entries[s])):
            if entries[s][i]["class"] == klasse:
                if entries[s][i]["day"] == wanted_day.capitalize():
                    lesson = entries[s][i]["lesson"]
                    new_subject = entries[s][i]["new_subject"]
                    room = entries[s][i]["room"]
                    old_subject = entries[s][i]["subject"]
                    teacher = entries[s][i]["new_teacher"]
                    vertreter = entries[s][i]["type"]
                    text = entries[s][i]["text"]
                    
                    final.append({"lesson": lesson, "new_subject": new_subject, "room": room, "old_subject": old_subject, "teacher": teacher, "type": vertreter, "text": text})

    message = f"Am {wanted_day.capitalize()} gibt es {str(len(final))} Einträge.\n"
    for s in final:
        message += f"lesson: {s['lesson']} | vertretung(?): {s['new_subject']} | new_subject: {s['room']} | room: {s['old_subject']} | teacher: {s['teacher']} | type: {s['type']} | text: {s['text']}  |x| "
    return message

if __name__ == '__main__':
    app.run()