import streamlit as st
from helper_functions import *
from youtube_transcript_api import YouTubeTranscriptApi
import numpy as np

# @st.cache_data
def get_transcript_list(_transcripts):
    st.session_state.transcripts = []
    for transcript in _transcripts:
        print(transcript)
        st.session_state.transcripts.append(transcript)

@st.cache_data
def generate_response(prompt):
    completions = openai.Completion.create(
        engine = "text-davinci-001",
        prompt = prompt,
        max_tokens = 100,
        n = 1,
        stop = None,
        temperature=0.5,
    )
    message = completions.choices[0].text
    return message 

@st.cache_data
def get_Summary(passage):
    response = openai.Completion.create(
                        engine="text-davinci-002",
                        prompt=f'Can you generate a summary for this passage : {passage}',
                        temperature=0.3,
                        max_tokens=100
                        )
    return response

def main():
    st.title("YouTube Podcast Summary and Visualization")
    api_key = st.text_input("Enter OpenAI API key")
    if api_key:
        openai.api_key = api_key

        # list models
        models = openai.Model.list()
        model = st.selectbox('Select Model', options = models.data)

        # check if your model works with simlple prompt
        prompt = st.text_input('Check if your Model Works with a prompt', value = 'Hello There!')
        st.write(generate_response(prompt))

    video_id = st.text_input("Enter YouTube video ID:")
    time_gap = st.number_input("Enter Time Resolution of Summary", value = 10.0)
    if video_id and api_key:
        transcript, listTranscript = get_transcript(video_id)
        if transcript == False:
            get_transcript_list(listTranscript)
            transcriptName = st.selectbox("Select Transcript", options = st.session_state.transcripts)
            transcript = YouTubeTranscriptApi.list_transcripts(video_id.split('?v=')[-1]).find_transcript(['en-US'])
            chunks, token_sizes = chunk_transcript(transcript, time_gap)
            mean = np.mean(np.array(token_sizes))
            st.write('Mean Token Size : ', mean)
            st.write('Number of requests : ', len(token_sizes))
            st.write(f'Assuming 0.03$/1K tokens, approximate cost is {mean*len(token_sizes)*0.03/1000} $')
        else:
            pass
        # st.write("Categories:", categories)
        generate = st.button('Generate Summary')
        if generate:
            # if transcript == False:
                
            
            summaries = []
            j = 0
            for chunk in chunks:
                j += 1
                if j>5:
                    break
                if 'summaries' not in st.session_state:
                    try:
                        st.write(f'Summary upto {round(chunk[1]/60)}')
                        response = get_Summary(chunk[0])
                        st.write(response.choices[0].text.strip())
                    except openai.error.Timeout as e:
                        # If rate limit error, sleep until the rate limits reset
                        st.write(f'Summary upto {round(chunk[1]/60)}')
                        time_to_sleep = e.reset - time.time()
                        time.sleep(time_to_sleep)

                        # Try the request again
                        response = get_Summary(chunk[0])
                        st.write(response.choices[0].text.strip())
                    summaries.append(response.choices[0].text.strip())
                else:
                    st.write(chunk)
                    st.write(st.session_state.summaries[j])
                    j += 1
                # st.write(summaries[-1])
            if 'summaries' not in st.session_state:
                st.session_state.summaries = summaries
            # summary = summarize(api_key, chunks) 
            # st.write("Summary:", summary)
        # Here you could add code to visualize the categories as a tree.
        # tree = create_tree(categories)  # You need to write the create_tree function.
        # st.pyplot(tree)

if __name__ == "__main__":
    main()
