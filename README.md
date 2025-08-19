AI-Powered LinkedIn Sales Automation Tool
This project is a functional prototype of an AI-powered platform designed to help sales teams and recruiters automate their LinkedIn outreach. The application takes user-defined campaign criteria, searches for relevant prospects on LinkedIn, analyzes their profiles using a Large Language Model, and generates hyper-personalized outreach messages.

✨ Core Features
Smart Prospecting: Dynamically searches LinkedIn for prospects based on job roles and location.
AI-Powered Profile Analysis: Leverages the Google Gemini API to read and understand the nuances of a user's profile, including their bio, work history, and recent activity.
Hyper-Personalized Messaging: Generates unique, context-aware connection messages for each prospect, referencing specific details from their profile to increase engagement.
Web-Based UI: A simple and clean single-page interface to define campaign parameters and view the generated results.

🛠️ System Architecture & Tech Stack
The application is built on a modern, decoupled architecture. A vanilla HTML/CSS/JS frontend communicates with a Python backend which orchestrates the scraping and AI generation tasks




<img width="3840" height="2221" alt="endToendFlow" src="https://github.com/user-attachments/assets/51b9e9dd-7cd8-4fab-bd8e-190c9ab2d533" />



Technologies Used:
Frontend: HTML, Bootstrap 5, Vanilla JavaScript
Backend: Python, FastAPI
Web Server: Uvicorn
Web Scraping: Selenium
AI & NLP: Google Gemini API

🚀 Getting Started
Follow these instructions to set up and run the project on your local machine.

1. Prerequisites
Python 3.9+
Git
Google Chrome browser

git clone https://github.com/YOUR_USERNAME/linkedin-sales-automation.git
cd linkedin-sales-automation

Step 2: Create and activate a virtual environment

On Windows (PowerShell):
python -m venv venv
.\venv\Scripts\activate

On macOS/Linux:
python3 -m venv venv
source venv/bin/activate

Step 3: Install dependencies
pip install -r requirements.txt

Step 4: Create your environment file
Create a new file named .env in the root of the project folder. This file will hold your secret credentials. This file is included in .gitignore and will not be committed to the repository.

Open the .env file and add the following lines, replacing the placeholder text with your actual credentials:
LINKEDIN_EMAIL="your_linkedin_email@example.com"
LINKEDIN_PASSWORD="your_linkedin_password"
GEMINI_API_KEY="your_google_ai_studio_api_key"

▶️ How to Run the Application
The application consists of two parts that need to be running simultaneously: the backend server and the frontend interface.

1. Start the Backend Server:
In your terminal (with the virtual environment activated), run the following command:
uvicorn main:app --reload

The server will start and be available at http://127.0.0.1:8000

2. Open the Frontend Interface:
Navigate to the project folder in your file explorer and double-click the index.html file to open it in your web browser.

📋 Usage
Once the index.html page is open, you will see the campaign setup form.
Fill in the criteria for your ideal prospect (e.g., "Founder", "Bengaluru").
Click the "Start Campaign" button.
The application will open Chrome browser windows to perform the search and profile scraping. This process may take several minutes.
Once complete, the results will be displayed as cards on the web page, showing the AI's thought process and the final personalized message for each prospect.


🔮 Future Improvements
This prototype successfully demonstrates the core "Context Engineering" pipeline. For a production-ready application, the following features would be the next steps:
Database Integration: Use a database like PostgreSQL to store campaign details, prospects, and generated messages.
Outreach Sequencing: Implement a task queue (e.g., Celery with Redis) to schedule the sending of connection requests and automated follow-up messages over time to mimic human behavior.
Response Dashboard: Build an analytics interface to track key metrics like connection rates, reply rates, and campaign ROI.
Enhanced Filtering: Improve the scraper to filter prospects by more advanced criteria like Company Size and industry tags.
