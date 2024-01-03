import numpy as np
import pandas as pd
import requests
import streamlit as st
from schedule import every, repeat
from natsort import index_natsorted


def get_notifications(port):
    # Replace with actual logic to fetch notifications
    if port != 'Select Port':
        response = requests.get(f"http://localhost:{port}/get_notifications")
        try:
            if response.status_code == 200:
                df = pd.DataFrame(response.json())
                df = df.sort_values(by='clip_idx', key=lambda x: np.argsort(index_natsorted(df["clip_idx"])), ascending=False)
                return df
            else:
                print(f"Failed to fetch notifications: {response.status_code}")
                return pd.DataFrame()
        except Exception as e:
            print(f'Exception {e}')
            return pd.DataFrame()
    return pd.DataFrame()


@repeat(every(10).seconds)
def show_notifications_feed(port=8000):
    st.markdown("""### Notification Feed""", unsafe_allow_html=True)

    notifications_placeholder = st.empty()

    notifications_df = get_notifications(port)

    html_content = ""
    with notifications_placeholder.container():
        st.markdown("""
            <style>
                section.main>div {
                    padding-bottom: 1rem;
                }
                [data-testid="stHorizontalBlock"] >div:nth-child(2)>div>div>div>div:nth-child(2) {
                    overflow: auto;
                    height: 40vh;
                }
            </style>
            """, unsafe_allow_html=True)

        for _, row in notifications_df.iterrows():
            if row['prediction'] != 'normal':
                video_url = row['clip_path']
                message = f"{row['prediction']} detected on {row['camera_name']} in {row['clip_idx']}"

                st.video(video_url, start_time=0)
                st.write(message)
