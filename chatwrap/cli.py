#Command line interface from ChatWrap

from argparse import ArgumentParser
import os
from chatwrap.client import LLMClient
from dotenv import load_dotenv

LLM_SERVER_URL = 'https://api.openai.com/v1/chat/completions'	


def cli(params): 
    load_dotenv()

    llmClient = LLMClient(LLM_SERVER_URL, os.getenv('OPENAI_API_KEY'))
    
    llmClient.send_request(params.prompt, params.model, params.temperature, params.streaming)
  
if __name__== "__main__":

    args = ArgumentParser('Chat Wrap')
    
    args.add_argument('prompt', help='prompt to use')
    args.add_argument('--version', action='version', version='%(prog)s 0.1')
    args.add_argument('--model', help='model to use', default='gpt-4o')
    args.add_argument('--temperature', help='temperature for sampling', default=0.7)
    args.add_argument('--streaming', action='store_true', help='streaming mode')


    params = args.parse_args()

    cli(params)

