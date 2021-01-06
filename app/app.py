import os
import datetime
from dateutil import tz
from dateutil.parser import parse
from flask import Flask, request, render_template
from functions import human_delta
from database import insert_activity, fetch_most_recent_activity, fetch_all_activities, reset_table, DB_NAME

app = Flask(__name__)

time_zone = tz.gettz()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/events', methods=['GET', 'POST'])
def events():
    if request.method == 'GET':
        most_recent_events = {k: parse(v) for k,v in fetch_most_recent_activity().items()}
        request_time = datetime.datetime.now(tz=time_zone)
        if len(most_recent_events) == 0:
            return render_template("no_history.html")
        else:
            time_since = {k: human_delta(request_time - t) for k,t in most_recent_events.items()}
            return render_template("most_recent_event.html", deltas = time_since, events = most_recent_events)

    if request.method == 'POST':
        data = request.json
        insert_activity(data)
        return "logged"

if __name__ == "__main__":
    if not os.path.isfile(DB_NAME):
        reset_table()

    app.run(host="0.0.0.0", debug=True, port=5000)