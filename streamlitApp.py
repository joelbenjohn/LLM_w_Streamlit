import streamlit as st
from helper_functions import *

def main():
    st.title("YouTube Podcast Summary and Visualization")

    video_id = st.text_input("Enter YouTube video ID:")

    if video_id:
        transcript = get_transcript(video_id)  # You need to write the get_transcript function.
        summary = summarize(transcript)  # You need to write the summarize function.
        categories = categorize(summary)  # You need to write the categorize function.

        st.write("Summary:", summary)
        st.write("Categories:", categories)

        # Here you could add code to visualize the categories as a tree.
        # tree = create_tree(categories)  # You need to write the create_tree function.
        # st.pyplot(tree)

if __name__ == "__main__":
    main()
