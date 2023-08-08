import streamlit as st
from helper_functions import *
from youtube_transcript_api import YouTubeTranscriptApi
import numpy as np
from summarizer import Summarizer
from transformers import pipeline

# @st.cache_data
## Save youtube video transcript to session state
def get_transcript_list(_transcripts):
    st.session_state.transcripts = []
    for transcript in _transcripts:
        print(transcript)
        st.session_state.transcripts.append(transcript)

# Cache prompt response calls to openAI API
# Function to check if openAI API works with api provided
@st.cache_data
def generate_response_openAI(prompt):
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

# @st.cache_resource
def selectModel(serviceName):
    st.session_state.generateSummary = True
    st.session_state.modelName = serviceName


@st.cache_resource
def load_bert_model():
    return Summarizer()

@st.cache_resource
def load_huggingFace_model():
    return pipeline('summarization')


@st.cache_data
def get_Summary(passage, serviceName):
    if serviceName == 'openAI':

        response = openai.Completion.create(
                            engine="text-davinci-002",
                            prompt=f'Can you generate a summary for this passage : {passage}',
                            temperature=0.3,
                            max_tokens=100
                            )
        response = response.choices[0].text.strip()

    elif serviceName == 'Bert':

        model = load_bert_model()
        response = model(passage, min_length=60, max_length=100)

    elif serviceName == 'HuggingFace Chat':

        model = load_huggingFace_model()
        response = model(passage, min_length=60, max_length=100)[0]['summary_text']

    return response

def main():

    st.title("YouTube Podcast Summary and Visualization")
    video_id = st.text_input("Enter YouTube video ID:")
    time_gap = st.number_input("Enter Time Resolution of Summary", value = 10.0)

    if video_id:

        transcript, listTranscript = get_transcript(video_id)
        if transcript == False:
            get_transcript_list(listTranscript)
            transcriptName = st.selectbox("Select Transcript", options = st.session_state.transcripts)
            transcript = YouTubeTranscriptApi.list_transcripts(video_id.split('?v=')[-1]).find_transcript(['en-US'])
            chunks, token_sizes = chunk_transcript(transcript.fetch(), time_gap*60)
            mean = np.mean(np.array(token_sizes))
            # st.write(transcript.fetch())
            st.write(['Transcript is manually created', 'Transcript is auto-generated'][transcript.is_generated])
            
        else:
            # st.write(transcript)
            st.write('Transcript is auto-generated')
            chunks, token_sizes = chunk_transcript(transcript, time_gap*60)
            mean = np.mean(np.array(token_sizes))
 
        openAITab, bertTab, huggingTab = st.tabs(['Open AI', 'Bert Extraction Summary', 'Hugging Face'])
        with openAITab:
            api_key = st.text_input("Enter OpenAI API key")
            st.markdown('###v Open AI API')
            st.write(' -Not Really Open Source and Not Really Free')
            st.write(' Expect 3$ charge for api calls with ChatGPT model to summarize a 2 hr Youtube podcast')
            if api_key:

                modelName = 'Open AI'
                openai.api_key = api_key

                # list models
                models = openai.Model.list()
                model = st.selectbox('Select Model', options = models.data)

                # check if your model works with simlple prompt
                prompt = st.text_input('Check if your Model Works with a prompt', value = 'Hello There!')
                st.write(generate_response_openAI(prompt))

                st.write('Mean Token Size : ', mean)
                st.write('Number of requests : ', len(token_sizes))
                st.write(f'Assuming 0.03 \$ 1K tokens, approximate cost is {mean*len(token_sizes)*0.03/1000} \$')
                generate = st.button('Generate Summary', key = 'openAIButton', on_click = selectModel, args = ['open AI'])

        with bertTab:
            st.markdown('### Bert Extraction Summary')
            st.write(' -Really Open Source and Really Free')
            modelName = 'Bert'
            generate = st.button('Generate Summary', key = 'bertButton', on_click = selectModel, args = ['Bert'] )

        with huggingTab:
            st.markdown('### HuggingFace Chat API')
            st.write(' -Really Open Source and Really Free')
            modelName = 'Bert'
            generate = st.button('Generate Summary', key = 'huggingButton', on_click = selectModel, args = ['HuggingFace Chat'])

        # st.write("Categories:", categories)
        if 'generateSummary' not in st.session_state:
            st.session_state.generateSummary = False

        if st.session_state.generateSummary:
            # if transcript == False:
                
            st.write(f'{st.session_state.modelName} Model Summary')
            summaries = []
            j = 0
            for chunk in chunks:
                j += 1
                if j>5:
                    break
                # if 'summaries' not in st.session_state:
                #     try:

                st.write(f'Summary upto {round(chunk[1]/60)}')
                st.write(f'Chunk {j}')
                st.write(chunk[0])
                response = get_Summary(chunk[0], st.session_state.modelName)
                st.write(response)
                st.divider()

                #     except Exception as e:

                #         st.write(e)
                #         # If rate limit error, sleep until the rate limits reset
                #         st.write(f'Summary upto {round(chunk[1]/60)}')
                #         time_to_sleep = e.reset - time.time()
                #         time.sleep(time_to_sleep)
                #         # Try the request again
                #         response = get_Summary(chunk[0], st.session_state.modelName)
                #         st.write(response)
                #     summaries.append(response)
                # else:
                #     st.write(f'Summary upto {round(chunk[1]/60)}')
                #     st.write(f'Chunk {j}')
                #     st.write(chunk[0])
                #     st.write(st.session_state.summaries[j])
                    # j += 1
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
