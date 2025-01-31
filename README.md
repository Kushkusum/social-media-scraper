# social-media-scraper
YouTube Data Scraper
This project is a YouTube data scraper built using Python, Tkinter for the GUI, and the YouTube Data API (v3). It allows users to extract various data from YouTube, including channel details and video comments. The data is saved in a CSV format for further analysis or processing.

Features
Channel Scraping:
Extracts details such as channel title, subscriber count, video count, and total view count.
Video Comment Scraping:
Extracts the comments from a specific YouTube video, including author name, comment text, and timestamp of when the comment was posted.
Saves the comments to a CSV file.
GUI Interface:
Simple Tkinter-based GUI to input YouTube URLs and display results.
Option to download the scraped data as a CSV file.

Technologies Used
Python: Main programming language.
Tkinter: GUI library for the application interface.
Google API Client: For interacting with the YouTube Data API (v3).
Pandas: For saving the data into a CSV file.

Setup
Prerequisites
Before running the project, ensure you have the following installed:
Python 3.x
Pip (Python package manager)

Installing Dependencies
Clone the repository to your local machine:
    git clone https://github.com/your-username/your-repository-name.git
    cd your-repository-name

Install the required Python packages:
    pip install -r requirements.txt


API Key Setup
You need to have a valid YouTube Data API key to interact with the YouTube API. To set up the API key:
Go to the Google Developers Console.
Create a new project and enable the YouTube Data API v3.
Get your API key from the Credentials section.
Create a .env file in the project root directory and add the following line:
    YOUTUBE_API_KEY=your-api-key-here


Running the Application
Once you have set up the API key, you can run the application by executing the following command:
    python app.py
The GUI will open, allowing you to input a YouTube URL. You can scrape either:

Channel Data: For channel URLs (e.g., https://youtube.com/channel/XXXX)
Video Comments: For video URLs (e.g., https://youtube.com/watch?v=XXXX)
After scraping the data, you will have the option to download the results as a CSV file.

Limitations
Followers/Following Data: Currently, the scraper does not support scraping followers or following data due to restrictions in the YouTube API. YouTube's API limits the available data, and follower/following information is not publicly accessible through the API.

Post Likes: YouTube does not provide direct access to the like data of individual comments or videos via the API. Therefore, this feature is not included in this scraper.


