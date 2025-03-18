# Holiday Let Cleaner Booking API

## Project Brief  
This project involves designing and implementing a **real-world API** to manage cleaning jobs for holiday rental properties. The system allows property owners to post cleaning jobs, and cleaners to accept jobs, clock in, and clock out.  

The API interacts with a **MySQL database** to store and retrieve cleaning job information, ensuring a seamless booking and tracking process for property owners and cleaners alike.  

## Description  
The **Holiday Let Cleaner Booking API** is a Flask-based application that facilitates booking and managing cleaning jobs for holiday rentals.  

### Features:  
- **Retrieve pending cleaning jobs** – Cleaners can view available jobs that need to be completed.  
- **Accept a cleaning job** – A cleaner can accept a job by providing their ID and confirming the work schedule.  
- **Clock in and out** – Cleaners can track their working hours by clocking in when they start a job and clocking out when they finish.  

This project demonstrates **API development, database interaction with MySQL, user authentication, and real-life application of RESTful principles**.  

✅ **This API was developed as part of a coding assignment to showcase database-driven API design.**  
✅ **Assignment Score:** **100%**  

---  

## Technologies Used  
- **Python** – API development using Flask  
- **MySQL** – Database for storing users, properties, and cleaning jobs  
- **Flask** – Framework for handling API requests  
- **Requests** – Client-side interaction with the API  
- **JSON** – Data format for API communication  

---  

## API Endpoints  

### 1. Get Pending Cleaning Jobs  
**Endpoint:** `/cleaningjobs` (GET)  
**Description:** Returns a list of all pending cleaning jobs.  

### 2. Accept a Cleaning Job  
**Endpoint:** `/accept_job` (POST)  
**Description:** Allows a cleaner to accept a job by providing their cleaner ID and job details.  

### 3. Clock In  
**Endpoint:** `/clockin` (POST)  
**Description:** Records when a cleaner starts a job.  

### 4. Clock Out  
**Endpoint:** `/clockout` (POST)  
**Description:** Records when a cleaner completes a job and calculates time worked.  

---  

## Setting Up and Running the API  

### **Installation Requirements**  
Ensure you have **Python 3**, **MySQL**, and **pip** installed.  

1. **Clone the repository:**  
   ```bash  
   git clone <repository-link>  
   cd holiday-let-cleaning-api  
   ```  

2. **Create and configure the database:**  
   - Import the provided SQL file into MySQL to set up the tables.  

3. **Install dependencies:**  
   ```bash  
   pip install -r requirements.txt  
   ```  

4. **Edit the config file:**  
   - Open `config.py` and enter your database credentials.  

5. **Run the API server:**  
   ```bash  
   python app.py  
   ```  
   The API will be available at `http://127.0.0.1:5001/`.  

6. **Run the client-side script:**  
   ```bash  
   python main.py  
   ```  
   Follow the on-screen instructions to interact with the API.  

---  

## Expected Behavior  

1. **View Available Jobs:**  
   - The system displays all cleaning jobs with job IDs, property details, and required cleaning time.  

2. **Accept a Job:**  
   - Cleaners enter their ID and job ID to accept a job. If the cleaner ID is invalid, an error is returned.  

3. **Clock In and Out:**  
   - Cleaners track their working hours, and the system calculates total time worked for payroll purposes.  

---  

## Example Interaction  

**User selects 'View Available Jobs':**  
```
Available Cleaning Jobs:  
ID    Date       Property ID     Time Needed  Linens    
------------------------------------------------------------  
101   Sat, 15 Mar 2025 00:00:00 GMT 20001           3 hrs        No    
102   Sun, 16 Mar 2025 00:00:00 GMT 20002           2 hrs        Yes    
```  

**User accepts a job:**  
```
Enter the Job ID you want to accept: 102  
Enter your Cleaner ID: 10005  
Enter your start time (HH:MM): 14:00  
Enter your end time (HH:MM): 16:00  

Response from server: {'message': 'Job accepted successfully!'}  
```  

**User clocks in:**  
```
Enter your Cleaner ID: 10005  
Enter the Job ID you are starting: 102  

Response from server: {'message': 'Clock-in successful!'}  
```  

---  

## Summary  
The **Holiday Let Cleaner Booking API** provides a streamlined system for property owners and cleaners to manage cleaning jobs efficiently. It ensures real-time job tracking, prevents unauthorised job acceptance, and allows accurate payroll calculation based on time worked.  

This project showcases **API development, MySQL integration, Flask framework, and real-world database applications**.  

---  



