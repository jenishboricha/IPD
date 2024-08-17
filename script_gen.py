import streamlit as st
from moviepy.editor import VideoFileClip, concatenate_videoclips
import requests
import google.generativeai as genai
import os
import re  # Import the re module for regular expressions

# Replace these with your actual API keys
PEXELS_API_KEY = "Oe8LHdq5GMhzMQHbgjJfgaFWycoe70Vm061rCg36wDYLf3d52t2SLoPi"
GENIE_API_KEY = "AIzaSyBzB-FbuQimtmUEoaXUwYdGoxUwTXvMO3I"

def get_gemini_response(question):
    try:
        # Configure the API key securely
        genai.configure(api_key="AIzaSyBzB-FbuQimtmUEoaXUwYdGoxUwTXvMO3I")

        # Initialize the generative model
        model = genai.GenerativeModel("gemini-pro")

        # Start a chat session
        chat = model.start_chat()

        # Send a message to the chat model
        response = chat.send_message(question, stream=True)

        # Collect and return the response text
        response_text = ""
        for message in response:
            # Print out the message to understand its structure
            st.write(message.text)
            # Extract the actual content of the message


        return response_text

    except Exception as e:
        print(f"Error occurred: {e}")
        return None


def extract_keywords(text):
    """Extract keywords or example phrases from the script."""
    if text:
        return re.findall(r'\b\w+\b', text)
    return []

def get_videos(topic, num_results=5):
    headers = {"Authorization": PEXELS_API_KEY}
    
    # Fetch videos based on the topic
    videos_url = "https://api.pexels.com/videos/search"
    params = {"query": topic, "per_page": num_results}
    try:
        response = requests.get(videos_url, headers=headers, params=params)
        response.raise_for_status()
        videos = [video["video_files"][0]["link"] for video in response.json().get("videos", [])]
    except Exception as e:
        st.error(f"Error fetching videos: {e}")
        videos = []

    return videos

def download_video(video_url, index):
    video_path = f"temp_video_{index}.mp4"
    try:
        response = requests.get(video_url)
        response.raise_for_status()
        with open(video_path, "wb") as f:
            f.write(response.content)
        return video_path
    except Exception as e:
        st.error(f"Error downloading video {video_url}: {e}")
        return None

def create_compilation(videos, output_file='compilation.mp4'):
    clips = []

    # Add video clips
    for idx, video_url in enumerate(videos):
        video_path = download_video(video_url, idx)
        if video_path:
            try:
                video_clip = VideoFileClip(video_path)
                clips.append(video_clip)
            except Exception as e:
                st.error(f"Error processing video {video_url}: {e}")

    if clips:
        try:
            final_clip = concatenate_videoclips(clips, method="compose")
            final_clip.write_videofile(output_file, fps=24)
        except Exception as e:
            st.error(f"Error creating video compilation: {e}")
    else:
        st.error("No clips to compile.")

    # Clean up temporary files
    for idx in range(len(videos)):
        video_path = f"temp_video_{idx}.mp4"
        if os.path.exists(video_path):
            os.remove(video_path)

# Streamlit app UI
st.title("Educational Script Generator")
st.write("Welcome")
st.write("Learn any topic easily")

# Input for the topic
topic = st.text_input("Enter the topic to learn")

# Slider for difficulty
difficulty = st.slider("Select 0 for easy and 1 for Hard", 0.0, 1.0, 0.0)

# Button to submit
submit = st.button("Submit")

if submit:
    if topic:
        st.write("Generating script, please wait...")

        difficulty_text = "easy" if difficulty < 0.5 else "hard"

        # Prompt construction
        prompt = f"Write a 300-word educational script for a video that explains the topic of '{topic}' at a {difficulty_text} difficulty level. Use clear and engaging language suitable for teenagers. Include at least two real-life examples to illustrate key concepts. Ensure the explanation is concise and maintains the audience's interest throughout the script."

        # Get the response from the Gemini model
        script = get_gemini_response(prompt)
        st.write(script)

        # Extract keywords for relevant videos
        keywords = extract_keywords(script)

        # Get relevant videos
        videos = get_videos(topic)
        st.write(f"Found {len(videos)} videos")

        # Create a compilation video
        st.write("Creating a video compilation, please wait...")
        create_compilation(videos)
        
        # Display the video compilation
        if os.path.exists("compilation.mp4"):
            st.write("### Compilation Video")
            st.video("compilation.mp4")
        else:
            st.write("No video compilation found.")
    else:
        st.write("Please enter a valid topic.")
