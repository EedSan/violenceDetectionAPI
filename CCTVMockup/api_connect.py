import requests
import streamlit as st
import socket


def is_port_open(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)  # Timeout for the socket connection
        try:
            s.connect((host, port))
            return True
        except socket.error as e:
            return False


# Function to list open ports (example range: 8000-9000)
def list_open_ports():
    host = "127.0.0.1"  # Localhost - modify as needed
    open_ports = []
    for port in range(8000, 9001):
        if is_port_open(host, port):
            open_ports.append(port)
    return open_ports


# Function to connect to API (placeholder - replace with your actual API call)
def connect_to_api(port):
    try:
        response = requests.get(f"http://localhost:{port}/")
        return response.status_code
    except Exception as e:
        return f"Error: {e}"


def submit_video_to_api(video_from_camera, port):
    # Placeholder function - replace with your actual API submission logic
    # For example, sending a POST request to the API with video data
    try:
        response = requests.post(f"http://localhost:{port}/upload", data={'video': video_from_camera})
        if response.status_code == 200:
            st.session_state['video_submitted'] = True
            return "Video submitted successfully"
        else:
            return "Failed to submit video"
    except Exception as e:
        return f"Error: {e}"
