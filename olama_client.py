import json
import requests
import re
# NOTE: ollama must be running for this to work, start the ollama app or run `ollama serve`
model = 'llama2' # TODO: update this for whatever model you wish to use

template = """
Imagine you are a worker whose job is to ask questions about what purpose funds transfer (international remittance) is to pay for, and you flag it accordingly. 
This will take the form of a explanatory note from a customer, and then it is flagged as Low, Mid or High risk. A reason may also be provided.

Some legitimate categories of remittance: 

1. **Family Support**: One of the most common reasons is to support family members living in another country. This can include money for everyday expenses, education, medical bills, or other emergencies.

2. **Paying for Goods and Services**: If someone buys goods or services from another country, they may need to make international payments to settle their bills.

3. **Tuition Fees**: Students studying abroad may need funds from their home country to pay for tuition, accommodation, and other living expenses.

4. **Real Estate Investments**: Purchasing property in another country may require sending large sums of money overseas.

5. **Travel**: Tourists may need to send money to pay for accommodation, tours, or other travel-related expenses ahead of their trip.

6. **Pension or Retirement**: Retirees living in another country might receive their pension from their home country.

7. **Salaries and Wages**: Employers may need to pay employees or contractors who reside in another country.

8. **Gifts or Inheritance**: Individuals might send money as a gift to loved ones abroad or as part of an inheritance.

9. **Charitable Donations**: Sending money to support a charitable cause or an NGO in another country.

10. **Business Investments**: Businesses may send money to invest in projects, joint ventures, or to set up a subsidiary in another country.

11. **Loan Repayments**: If an individual has taken a loan from a foreign entity, they might need to make periodic repayments, which would involve international transfers.

12. **Royalties and Licensing Fees**: Companies or individuals might have to make international transfers to pay for intellectual property use, like for music, patents, or trademarks.

13. **Dividends and Profit Repatriation**: Businesses with international operations might send profits back to their home country or to international shareholders.

14. **Immigration or Emigration**: Individuals moving to a new country might transfer their savings or assets.

15. **Paying for Medical Services**: Someone might go to another country for medical treatment and need to transfer money to pay for these services.

16. **Tax Payments**: Paying taxes or fees to foreign governments.

17. **Subscription Services**: Paying for international subscriptions, like magazines, software, or online services.

18. **Freelancing or Online Work**: With the growth of the gig economy, many individuals offer their services online and get paid from clients around the world.

Some categories which may require further investifation and be flagged as high: 

Money laundering and terrorism financing are illegal activities that involve moving funds to make their origins harder to trace or to support illicit actions. While it's crucial to approach this topic with sensitivity, it's equally essential to be aware of some "fronts" or seemingly legitimate reasons that could be used to obscure such activities. Here are some reasons or methods that have historically been misused:

1. **Trade-Based Laundering**: Over-invoicing or under-invoicing of goods and services can be a way to move money illicitly across borders.

2. **Real Estate Transactions**: Buying properties can be a way to "clean" large amounts of money. The property can then be sold, and the proceeds will appear legitimate.

3. **Shell Companies and Trusts**: These entities can be set up to hide the true ownership of funds.

4. **Offshore Accounts**: Banking in jurisdictions with strict secrecy laws can hide the origins of money.

5. **Purchase of Expensive Goods**: Buying items like art, jewelry, or luxury cars can be used to launder money.

6. **Casinos**: Using funds to buy chips, only to cash them out later, can make funds seem like legitimate winnings.

7. **Loans**: Fake or sham loans can be used where no actual money is transferred, but paperwork is created to make it seem like legitimate transactions occurred.

8. **Digital and Cryptocurrencies**: Cryptocurrencies can be used due to their perceived anonymity and decentralized nature.

9. **Gifts or Inheritance**: Claiming large sums of money as gifts or inheritance can sometimes be a cover for illicit funds.

10. **Fake Charities**: Setting up or using bogus charities to move money can obscure the source or intended use of funds.

11. **Investments in Legitimate Businesses**: Injecting illicit funds into legitimate businesses and then extracting them as legitimate earnings.

12. **"Smurfing" or "Structuring"**: Depositing smaller amounts of money regularly to avoid suspicion or reporting thresholds.

13. **Using Intermediaries**: Employing a network of individuals (often without their knowledge) to make multiple small transactions on behalf of the launderer.

14. **Crowdfunding or Online Platforms**: Using online platforms to raise funds under the pretext of a legitimate cause or business venture.


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
Explanation: $EXP"""


def pull_model():
    print("checking if model is available and fetching if not")
    url = 'http://localhost:11434/api/pull'
    headers = {'Content-Type': 'application/json'}
    data = {
        "name": "llama2:7b"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    print(response.text)

def generate(explanation, context):
    
    prompt = template.replace('$EXP', explanation)
    

    r = requests.post('http://localhost:11434/api/generate',
                      json={
                          'model': model,
                          'prompt': prompt,
                          'system': 'You are a scoring app that validates explanations for remittance funds transfer',
                          'context': context,
                      },
                      stream=True)
    r.raise_for_status()

    response = ''

    for line in r.iter_lines():
        body = json.loads(line)
        response_part = body.get('response', '')
        # the response streams one token at a time, print that as we recieve it
        print(response_part, end='', flush=True)

        response = response + response_part

        if 'error' in body:
            raise Exception(body['error'])

        if body.get('done', False):
            return extract_reason(response.strip()), body['context']
        
def extract_reason(text):
    # Use the DOTALL flag which makes the '.' special character match any character, including a newline
    flag_match = re.search(r'Flag: (.+?)\n', text, re.DOTALL)
    reason_match = re.search(r'Reason: (.+?)(\n\n|$)', text, re.DOTALL)  # Either two newlines or end of string indicates the end of the reason

    # Extract values if matches are found
    flag_value = flag_match.group(1).strip() if flag_match else None
    reason_value = reason_match.group(1).strip() if reason_match else None

    # Create an object (dictionary in this case) with the extracted values
    result = {
        'Flag': flag_value,
        'Reason': reason_value
    }            
    return result

def main():
    pull_model()
    context = [] # the context stores a conversation history, you can use this to make the model more context aware
    explanation = "Monthly allowance for my son"
    
    resp, context = generate(explanation=explanation, context=context)
    print("\n\n\ntotal response", resp)

if __name__ == "__main__":
    main()
