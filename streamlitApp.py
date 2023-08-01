import streamlit as st
from helper_functions import *

def main():
    st.title("YouTube Podcast Summary and Visualization")
    api_key = st.text_input("Enter OpenAI API key")
    video_id = st.text_input("Enter YouTube video ID:")
    time_gap = st.number_input("Enter Time Resolution of Summary", default = 10.0)
    if video_id:
        transcript = get_transcript(video_id)  # You need to write the get_transcript function.
        chunks = chunk_transcript(transcript, time_gap)
        summary = summarize(api_key, chunks)  # You need to write the summarize function.
        # categories = categorize(summary)  # You need to write the categorize function.

        st.write("Summary:", summary)
        # st.write("Categories:", categories)

        # Here you could add code to visualize the categories as a tree.
        # tree = create_tree(categories)  # You need to write the create_tree function.
        # st.pyplot(tree)

if __name__ == "__main__":
    main()
