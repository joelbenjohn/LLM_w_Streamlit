from youtube_transcript_api import YouTubeTranscriptApi

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

# Function to summarize text
def summarize(api_key: str, chunks: List[str]) -> List[str]:
    """Function to summarize chunks using OpenAI's GPT-4"""
    summaries = []
    openai.api_key = api_key

    for chunk in chunks:
        response = openai.Completion.create(
          engine="text-davinci-002",
          prompt=chunk,
          temperature=0.3,
          max_tokens=100
        )
        summaries.append(response.choices[0].text.strip())
    return summaries


# Fetch the transcript
# video_id = '883R3JlZHXE'

def makeContentChain(video_id)

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
