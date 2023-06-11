import os
import logging
import slack
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up Slack client
slack_token = os.environ.get('SLACK_API_TOKEN')  # Replace with your Slack API token or set it as an environment variable
client = slack.WebClient(token=slack_token)

# Set up ChatGPT API endpoint
gpt_api_endpoint = 'https://api.openai.com/v1/engines/davinci-codex/completions'

# Keyword to trigger ChatGPT search
keyword = '!GPT'

# Function to handle incoming messages
def handle_message(event):
    message = event['text']
    channel = event['channel']
    user = event['user']

    if keyword in message:
        query = message.replace(keyword, '').strip()
        logging.info(f'Received search query "{query}" from user {user} in channel {channel}')

        # Call ChatGPT API
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {os.environ["GPT_API_TOKEN"]}'  # Replace with your ChatGPT API token or set it as an environment variable
        }
        data = {
            'prompt': query,
            'max_tokens': 50  # Adjust the number of tokens based on the desired response length
        }
        response = requests.post(gpt_api_endpoint, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()['choices'][0]['text']
            logging.info(f'ChatGPT response: "{result}"')
            send_message(result, channel, thread_ts=event.get('ts'))
        else:
            logging.error(f'Error calling ChatGPT API: {response.text}')

# Function to send a message to Slack channel
def send_message(message, channel, thread_ts=None):
    response = client.chat_postMessage(channel=channel, text=message, thread_ts=thread_ts)

    if not response['ok']:
        logging.error(f'Error sending message to Slack channel: {response["error"]}')

# Main event loop
if __name__ == '__main__':
    @slack.RTMClient.run_on(event='message')
    def handle_rtm_message(**payload):
        handle_message(payload['data'])

    logging.info('Starting Slack RTM client...')
    slack_token = os.environ.get('SLACK_API_TOKEN')
    rtm_client = slack.RTMClient(token=slack_token)
    rtm_client.start()
