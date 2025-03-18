# You will need a config.py file containing your MySQL Workbench connection details
# USER = "YourUserName"
# PASSWORD = "YourPassword"
# HOST = "YourLocalHost"
# DATABASE = "holiday_clean"

import mysql.connector
from config import USER, PASSWORD, HOST, DATABASE
from datetime import datetime, timedelta


class DbConnectionError(Exception):
    pass


# Connect to the database
def connect_to_db():
    try:
        cnx = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE,
            auth_plugin='mysql_native_password'
        )
        return cnx
    except mysql.connector.Error as err:
        print(f'Database Connection Error: {err}')
        return None


# Get all pending cleaning jobs
def get_pending_jobs():
    jobs = []
    connection = connect_to_db()
    if not connection:
        return []

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM cleaning_job WHERE job_status = 'Pending'")
        jobs = cursor.fetchall()

        # Convert timedelta objects
        for job in jobs:
            if isinstance(job['check_in_time'], timedelta):
                job['check_in_time'] = str(job['check_in_time'])[:-3]
            if isinstance(job['check_out_time'], timedelta):
                job['check_out_time'] = str(job['check_out_time'])[:-3]

        return jobs

    except Exception:
        raise DbConnectionError("Failed to fetch cleaning jobs")
    finally:
        cursor.close()
        connection.close()


# Accept a cleaning job with validation for valid job ID and cleaner ID
def accept_cleaning_job(job_id, cleaner_id, start_time, end_time):
    # Fetch available jobs
    available_jobs = get_pending_jobs()

    # Check if the job ID exists in the available jobs
    job_exists = any(job['job_id'] == int(job_id) for job in available_jobs)

    if not job_exists:
        return {"error": "Invalid Job ID. The job doesn't exist or has already been taken."}

    # Validate cleaner ID by checking the users table for the user type 'Cleaner'
    connection = connect_to_db()
    if not connection:
        return {"error": "Database connection failed."}

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM users 
            WHERE user_id = %s AND user_type = 'Cleaner'
        """, (cleaner_id,))
        cleaner = cursor.fetchone()  # Fetch one row

        if not cleaner:
            return {"error": "Invalid Cleaner ID. The cleaner ID doesn't exist or is not assigned as a cleaner."}

        # Proceed to update the job status
        job_details = {
            "job_id": job_id,
            "cleaner_id": cleaner_id,
            "start_time": start_time,
            "end_time": end_time
        }

        result = requests.post(
            'http://127.0.0.1:5001/accept_job',
            headers={'Content-Type': 'application/json'},
            data=json.dumps(job_details)
        )

        if result.status_code == 200:
            return result.json()
        else:
            print(f"Error: {result.status_code}, Response: {result.text}")
            return {"error": "Failed to accept job"}

    except Exception as e:
        return {"error": f"Error validating cleaner ID: {str(e)}"}
    finally:
        cursor.close()
        connection.close()


# Clock-in the cleaner at the start of the job
def clock_in(cleaner_id, job_id):
    connection = connect_to_db()
    if not connection:
        return "Database connection failed."

    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO clocking_in_out (cleaner_id, job_id, clock_in_time)
            VALUES (%s, %s, NOW())
        """, (cleaner_id, job_id))
        connection.commit()
        return "Clock-in successful!"
    except Exception:
        raise DbConnectionError("Failed to clock-in.")
    finally:
        cursor.close()
        connection.close()


# Clock-out the cleaner at the end of the job and calculate time worked
def clock_out(cleaner_id, job_id):
    connection = connect_to_db()
    if not connection:
        return "Database connection failed."

    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE clocking_in_out
            SET clock_out_time = NOW(),
                total_work_time = TIMESTAMPDIFF(MINUTE, clock_in_time, NOW())
            WHERE cleaner_id = %s AND job_id = %s AND clock_out_time IS NULL
        """, (cleaner_id, job_id))
        connection.commit()

        # Now update the job status to 'Completed' in the cleaning_job table
        cursor.execute("""
            UPDATE cleaning_job
            SET job_status = 'Completed'
            WHERE job_id = %s
        """, (job_id,))
        connection.commit()

        return "Clock-out successful!"
    except Exception:
        raise DbConnectionError("Failed to clock-out.")
    finally:
        cursor.close()
        connection.close()

