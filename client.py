import json
import requests

# NOTE: ollama must be running for this to work, start the ollama app or run `ollama serve`
model = 'llama2' # TODO: update this for whatever model you wish to use

template = """
Imagine you are a worker whose job is to ask questions about what purpose funds transfer (international remittance) is to pay for, and you flag it accordingly. This will take the form of a explanatory note from a customer, and then it is flagged as Low, Mid or High risk. And reason may also be provided. 

For example: 

Explanation: To pay for cheese to for my uncle
Flag: Mid

Explanation: None of your business
Flag: High

Explanation: Share sale
Flag: Low

Explanation: Business proceeds
Flag: Med

Explanation: Business proceeds from newspaper stand
Flag: Low

Now classify this. Please ensure to prefix with "Flag" and "Reason" as appropriate: 
Explanation: Monthly allowance for my son
Flag:"""


def generate(prompt, context):
    r = requests.post('http://localhost:11434/api/generate',
                      json={
                          'model': model,
                          'prompt': prompt,
                          'system': 'You are a scoring app that validates explanations for remittance funds transfer',
                          'context': context,
                      },
                      stream=True)
    r.raise_for_status()

    for line in r.iter_lines():
        body = json.loads(line)
        response_part = body.get('response', '')
        # the response streams one token at a time, print that as we recieve it
        print(response_part, end='', flush=True)

        if 'error' in body:
            raise Exception(body['error'])

        if body.get('done', False):
            return body['context']

def main():
    context = [] # the context stores a conversation history, you can use this to make the model more context aware
    context = generate(template, context)

if __name__ == "__main__":
    main()
