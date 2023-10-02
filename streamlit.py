# main.py

import streamlit as st
import time
from olama_client import generate, pull_model


def process_input(explanation):
    print(explanation)
    response, _context = generate(explanation=explanation, context=[])
    return response

def main():
    st.title('Remittance Explanation App')

    # Input field for the explanation for remittance
    explanation = st.text_input('Explanation for remittance', '')

    # Button to process the explanation
    if st.button('Submit'):
        with st.spinner('Processing...'):
            result = process_input(explanation)
        st.json(result)

@st.cache_data
def load_model():
    pull_model()

if __name__ == '__main__':
    load_model()
    main()
