from youtube_transcript_api import YouTubeTranscriptApi
import openai
from typing import List
import time


# Function to guess the speaker based on the text
def guess_speaker(text):
    # Implement your speaker guessing logic here
    speaker = "..."
    return speaker

# Function to guess the context based on the text
def guess_context(text):
    # Implement your context guessing logic here
    context = "..."
    return context

def chunk_transcript(transcript: List[dict], time_gap: int) -> List[str]:
    """Function to split transcript into chunks based on time gap"""
    chunks = []
    token_sizes = []
    chunk = ''
    transcript = transcript.fetch()
    print(transcript, type(transcript))
    last_end_time = 0.0
    for section in transcript:
        # print(section['start'])
        if section['start'] - last_end_time > time_gap:
            chunks.append([chunk, section['start']])
            token_sizes.append(len(chunk))
            chunk = section['text']
        else:
            chunk += ' ' + section['text']
        last_end_time = section['start'] + section['duration']
    chunks.append([chunk, last_end_time])  # Don't forget the last chunk
    return chunks, token_sizes
    
def summarize(api_key: str, chunks: List[str]) -> List[str]:
    """Function to summarize chunks using OpenAI's GPT-4"""
    summaries = []
    openai.api_key = api_key

    for chunk in chunks:
        chunk = chunk[0]
        try:
            response = openai.Completion.create(
            engine="text-davinci-002",
            prompt='Summarize this passage for me : {chunk}',
            temperature=0.3,
            max_tokens=100
            )
        except openai.error.Timeout as e:
            # If rate limit error, sleep until the rate limits reset
            time_to_sleep = e.reset - time.time()
            time.sleep(time_to_sleep)

            # Try the request again
            response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=chunk,
            temperature=0.3,
            max_tokens=100
            )
        summaries.append(response.choices[0].text.strip())
    return summaries

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id.split('?v=')[-1])
    except:
        transcript = False
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id.split('?v=')[-1])

    return transcript, transcript_list

# Fetch the transcript
# video_id = '883R3JlZHXE'

def makeContentChain(video_id):

    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    
    # Initialize the blockchain
    blockchain = []
    
    # Iterate over the transcript
    for i in range(len(transcript)):
        # Get the current element
        current_element = transcript[i]
    
        # Guess the speaker and the context
        speaker = guess_speaker(current_element['text'])
        context = guess_context(current_element['text'])
    
        # If the blockchain is not empty
        if blockchain:
            # Get the last block in the blockchain
            last_block = blockchain[-1]
    
            # If the speaker and the context are the same as the last block
            if speaker == last_block['speaker'] and context == last_block['context']:
                # Append the current element to the last block
                last_block['text'] += ' ' + current_element['text']
                last_block['summary'] = summarize_text(last_block['text'])
            else:
                # Create a new block and add it to the blockchain
                block = {
                    'speaker': speaker,
                    'context': context,
                    'text': current_element['text'],
                    'summary': summarize_text(current_element['text'])
                }
                blockchain.append(block)
        else:
            # If the blockchain is empty, create the first block
            block = {
                'speaker': speaker,
                'context': context,
                'text': current_element['text'],
                'summary': summarize_text(current_element['text'])
            }
            blockchain.append(block)
    return blockchain
    # # Print the blockchain
    # for block in blockchain:
    #     print(block)
