
import tkinter as tk
from tkinter import messagebox, filedialog
from googleapiclient.discovery import build
import pandas as pd
import re
from dotenv import load_dotenv # type: ignore
import os

# Load environment variables from the .env file
load_dotenv()

# Access the API key from the environment
API_KEY = os.getenv("YOUTUBE_API_KEY")

# Build the YouTube API client
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Initialize Tkinter root window
root = tk.Tk()
root.title("YouTube Scraper")
root.geometry("500x400")
root.configure(bg="#f4f4f9")

# Function to extract channel ID from URL
def extract_channel_id(url):
    if "youtube.com/channel/" in url:
        # Extract channel ID from URL
        channel_id = url.split('/channel/')[1]
    elif "youtube.com/c/" in url:
        # Extract custom channel name
        channel_name = url.split('/c/')[1]
        channel_id = get_channel_id_by_name(channel_name)
    else:
        raise ValueError("Invalid YouTube Channel URL")
    return channel_id

# Function to get channel details
def get_channel_details(channel_id):
    request = youtube.channels().list(
        part="snippet,statistics",
        id=channel_id
    )
    response = request.execute()
    
    channel_info = []
    for item in response['items']:
        title = item['snippet']['title']
        subscribers = item['statistics']['subscriberCount']
        videos = item['statistics']['videoCount']
        views = item['statistics']['viewCount']

        channel_info.append({
            "Channel Title": title,
            "Subscribers": subscribers,
            "Videos": videos,
            "Views": views
        })
    
    return channel_info

# Function to get channel ID by name (for custom URLs)
def get_channel_id_by_name(channel_name):
    request = youtube.search().list(
        part="snippet",
        q=channel_name,
        type="channel"
    )
    response = request.execute()
    if "items" in response:
        return response['items'][0]['id']['channelId']
    else:
        raise ValueError("Channel not found")

# Function to extract video ID from URL
def extract_video_id(url):
    match = re.search(r"v=([a-zA-Z0-9_-]+)", url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid YouTube Video URL")

# Function to get video comments
def get_video_comments(video_id):
    comment_data = []
    next_page_token = None

    while True:
        try:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                pageToken=next_page_token
            )
            response = request.execute()

            # Loop through the comment items and extract the details
            for item in response['items']:
                author = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                published_at = item['snippet']['topLevelComment']['snippet']['publishedAt']  # Timestamp of comment
                comment_data.append({"Author": author, "Comment": comment, "Timestamp": published_at})

            # Check if there's another page of comments
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break  # Exit if there are no more pages

        except Exception as e:
            messagebox.showerror("Error", f"Error fetching comments: {e}")
            break

    return comment_data

# Function to save comments to a CSV file
def save_comments_to_csv(comments, filename="video_comments.csv"):
    # Convert the comment data into a pandas DataFrame
    df = pd.DataFrame(comments)
    # Save the DataFrame to a CSV file
    df.to_csv(filename, index=False)
    return filename

# Function to handle the button click event
def scrape_and_download():
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Input Error", "Please enter a valid YouTube URL")
        return

    try:
        if "youtube.com/channel/" in url or "youtube.com/c/" in url:
            # It's a channel URL
            channel_id = extract_channel_id(url)
            channel_details = get_channel_details(channel_id)
            # Output channel details
            result_text.delete(1.0, tk.END)
            for info in channel_details:
                result_text.insert(tk.END, f"Channel Title: {info['Channel Title']}\n")
                result_text.insert(tk.END, f"Subscribers: {info['Subscribers']}\n")
                result_text.insert(tk.END, f"Videos: {info['Videos']}\n")
                result_text.insert(tk.END, f"Views: {info['Views']}\n\n")

        elif "youtube.com/watch" in url:
            # It's a video URL
            video_id = extract_video_id(url)
            video_comments = get_video_comments(video_id)
            if video_comments:
                # Save the comments to CSV
                filename = save_comments_to_csv(video_comments)
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"Comments saved to {filename}")
                download_button["state"] = "normal"  # Enable the download button
            else:
                messagebox.showwarning("No Comments", "No comments found for this video.")
        else:
            raise ValueError("Invalid YouTube URL")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to allow the user to download the CSV file
def download_file():
    filename = "video_comments.csv"
    file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if file:
        messagebox.showinfo("Download", f"File saved as {file}")

# Create GUI Elements with Improved Styles
url_label = tk.Label(root, text="Enter YouTube URL:", font=("Arial", 12), bg="#f4f4f9")
url_label.pack(pady=10)

url_entry = tk.Entry(root, width=40, font=("Arial", 12))
url_entry.pack(pady=5)

scrape_button = tk.Button(root, text="Scrape Data", command=scrape_and_download, font=("Arial", 12), bg="#4CAF50", fg="white", relief="solid", width=20)
scrape_button.pack(pady=10)

result_text = tk.Text(root, width=50, height=10, font=("Arial", 10), bg="#e9f5f0", wrap="word", relief="solid")
result_text.pack(pady=10)

download_button = tk.Button(root, text="Download CSV", command=download_file, font=("Arial", 12), bg="#2196F3", fg="white", relief="solid", width=20, state="disabled")
download_button.pack(pady=10)

# Run the GUI
root.mainloop()
