import requests
import json
from db_utils import get_pending_jobs, accept_cleaning_job, clock_in, clock_out


# Get all the pending cleaning jobs
def get_pending_jobs():
    result = requests.get(
        'http://127.0.0.1:5001/cleaningjobs',
        headers={'content-type': 'application/json'}
    )
    return result.json()

# Accept a cleaning job
def accept_cleaning_job(job_id, cleaner_id, start_time, end_time):
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
        response = result.json()
        # Check for any errors in the response
        if 'error' in response:
            print(f"Error: {response['error']}")
            return response
        else:
            print(f"Success: {response['message']}")
            return response
    else:
        print(f"Error: {result.status_code}, Response: {result.text}")
        return {"error": "Failed to accept job"}

# Display available jobs in a formatted table
def display_jobs(jobs):
    print("\nAvailable Cleaning Jobs:")
    print("{:<5} {:<10} {:<15} {:<12} {:<8}".format(
        "ID", "Date", "Property ID", "Time Needed", "Linens"
    ))
    print("-" * 60)

    for job in jobs:
        print("{:<5} {:<10} {:<15} {:<12} {:<8}".format(
            job['job_id'], job['clean_date'], job['property_id'],
            f"{job['expected_clean_time']} hrs", job['linens_provided']
        ))

def run():
    print('##########################################')
    print('Welcome to the Holiday Let Cleaning System')
    print('##########################################\n')

    while True:
        print("\nSelect an option:")
        print("1. View Available Jobs")
        print("2. Clock In")
        print("3. Clock Out")
        print("4. Exit")

        choice = input("\nEnter the number of your choice: ")

        if choice == "1":
            # Display jobs and allow selection
            jobs = get_pending_jobs()
            display_jobs(jobs)

            job_choice = input("\nEnter the Job ID you want to accept: ")
            cleaner_id = input("Enter your Cleaner ID: ")
            start_time = input("Enter your start time (HH:MM): ")
            end_time = input("Enter your end time (HH:MM): ")

            response = accept_cleaning_job(job_choice, cleaner_id, start_time, end_time)
            # Check if the response contains an error
            if 'error' in response:
                print(f"Failed to accept job: {response['error']}")
            else:
                print(f"Job accepted successfully: {response['message']}")

        elif choice == "2":
            # Clock in
            cleaner_id = input("\nEnter your Cleaner ID: ")
            job_id = input("Enter the Job ID you are starting: ")

            response = clock_in(cleaner_id, job_id)
            print("\nResponse from server:", response)

        elif choice == "3":
            # Clock out
            cleaner_id = input("\nEnter your Cleaner ID: ")
            job_id = input("Enter the Job ID you are finishing: ")

            response = clock_out(cleaner_id, job_id)
            print("\nResponse from server:", response)

        elif choice == "4":
            print("\nGoodbye! Have a great day!")
            break  # Exit the loop

        else:
            print("\nInvalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == '__main__':
    run()
