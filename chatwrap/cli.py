#Command line interface from ChatWrap

from argparse import ArgumentParser
from chatwrap.client import LLMClient

LLM_SERVER_URL = 'http://127.0.0.1:1234/v1'

def cli(params): 
    print(params.prompt)
    
    llmClient = LLMClient(LLM_SERVER_URL)
    
    llmClient.send_request(params.prompt, params.model, params.temperature, params.streaming)
    llmClient.send_request(params.prompt, params.model, params.temperature, params.streaming)

    print(f'Total number {llmClient.totalNoOfTokens}')

if __name__== "__main__":

    args = ArgumentParser('Chat Wrap')
    
    args.add_argument('prompt', help='prompt to use')
    args.add_argument('--version', action='version', version='%(prog)s 0.1')
    args.add_argument('--model', help='model to use', default='qwen2.5-coder-0.5b-instruct')
    args.add_argument('--temperature', help='temperature for sampling', default=0.7)
    args.add_argument('--streaming', action='store_true', help='streaming mode')


    params = args.parse_args()

    cli(params)

