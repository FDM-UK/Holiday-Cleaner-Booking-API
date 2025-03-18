from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import json
from db_utils import get_pending_jobs, accept_cleaning_job, clock_in, clock_out

app = Flask(__name__)


# Custom JSON Encoder to handle timedelta and datetime
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, timedelta):
            return str(obj)  # Format timedelta as a string
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')  # Format datetime
        return super().default(obj)


# Tell Flask to use the custom encoder
app.json_encoder = CustomJSONEncoder


@app.route('/')
def index():
    return "Holiday Let Cleaner Booking API is up and running."


# Get all pending cleaning jobs
@app.route('/cleaningjobs')
def get_cleaning_jobs():
    jobs = get_pending_jobs()

    # Convert timedelta and decimal values before returning
    for job in jobs:
        job['check_in_time'] = str(job['check_in_time'])[:-3]  # Remove seconds
        job['check_out_time'] = str(job['check_out_time'])[:-3]
        job['rate_per_hour'] = float(job['rate_per_hour'])  # Convert Decimal to float

    return jsonify(jobs)


# Accept a cleaning job
@app.route('/accept_job', methods=['POST'])
def accept_job():
    data = request.get_json()

    job_id = data.get("job_id")
    cleaner_id = data.get("cleaner_id")
    start_time = data.get("start_time")
    end_time = data.get("end_time")

    response = accept_cleaning_job(job_id, cleaner_id, start_time, end_time)

    return jsonify({"message": response})



# Clock in a cleaner
@app.route('/clockin', methods=['POST'])
def clock_in_cleaner():
    data = request.get_json()
    result = clock_in(data['cleaner_id'], data['job_id'])
    return jsonify({"message": result})


# Clock out a cleaner
@app.route('/clockout', methods=['POST'])
def clock_out_cleaner():
    data = request.get_json()
    result = clock_out(data['cleaner_id'], data['job_id'])
    return jsonify({"message": result})


if __name__ == '__main__':
    app.run(debug=True, port=5001)
