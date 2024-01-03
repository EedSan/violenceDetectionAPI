import streamlit as st


def show_main_video_container(global_cam_list):
    n_videos = len(global_cam_list)

    if n_videos == 1:
        # For a single video, center it
        width = 50
        side = (100 - width) / 2
        _, video_container, _ = st.columns([side, width, side])
        video_path_ = f"CCTVMockup/resources/cctv_{global_cam_list[0]}_video.mp4"
        video_container.video(video_path_, start_time=0)
    else:
        # For multiple videos, display them in rows of 2

        for i in range(0, n_videos, 2):
            cols = st.columns(2)  # Create 2 columns
            for j in range(2):
                cols[j].write(f'''
                    <style>
                        .stVideo {{
                            height: 10hv;  /* Adjust the height as needed */
                            width: 100%;
                        }}
                    </style>
                    ''', unsafe_allow_html=True)
                if i + j < n_videos:
                    video_path_ = f"CCTVMockup/resources/cctv_{global_cam_list[i + j]}_video.mp4"
                    cols[j].video(video_path_, start_time=0)
