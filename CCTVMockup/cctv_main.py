import time

import streamlit as st

from api_connect import list_open_ports, connect_to_api, submit_video_to_api
from api_notifications import show_notifications_feed
from main_video_container import show_main_video_container

# Setting up the Streamlit layout
st.set_page_config(layout="wide")

GLOBAL_CAMERA_LIST = [f"camera{i}" for i in range(2)]

if 'api_connection_status' not in st.session_state:
    st.session_state['api_connection_status'] = None
if 'selected_cameras' not in st.session_state:
    st.session_state['selected_cameras'] = []
if 'last_connected_port' not in st.session_state:
    st.session_state['last_connected_port'] = None
if 'last_update_time' not in st.session_state:
    st.session_state['last_update_time'] = time.time()
if 'refresh_notifications' not in st.session_state:
    st.session_state['refresh_notifications'] = False


show_main_video_container(GLOBAL_CAMERA_LIST)
col1, col2 = st.columns(2)

# API Connection Status
with col1:
    st.markdown("""### API Connection""", unsafe_allow_html=True)

    open_ports = ['Select Port'] + list_open_ports()
    selected_port = st.selectbox("Select Port", open_ports)

    if selected_port != 'Select Port':
        st.session_state['api_connection_status'] = connect_to_api(selected_port)
        st.write(f"Status: {st.session_state['api_connection_status']}")

        if str(st.session_state['api_connection_status']).startswith('2'):
            # Camera selection
            with st.form('form1'):
                cameras = GLOBAL_CAMERA_LIST
                st.session_state['selected_cameras'] = st.multiselect("Select Cameras", cameras)

                # Submit button
                if st.form_submit_button("Submit Videos"):
                    for camera in st.session_state['selected_cameras']:
                        video_from_camera_path_ = f"CCTVMockup/resources/cctv_{camera}_video.mp4"
                        submit_status = submit_video_to_api(video_from_camera_path_, selected_port)
                        st.write(f"{camera}: {submit_status}")
                        st.session_state['video_submitted'] = True


# Notification Feed
with col2:
    show_notifications_feed(selected_port)
