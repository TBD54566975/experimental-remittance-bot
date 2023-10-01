# Remittance risk flagging app

*Experimental*

This app uses llama2 to show a ChatGPT competitive app to score remittance descriptions. Ie a human explains what they are transferring funds for and it comes up with a High,Low or Med score and reason for flagging for a further screening perhaps by another human (or to apply other rules). 

Uses<a href="https://ai.meta.com/llama/">llama2</a> model (7b also works ok) so it can run on modest hardware. 

NOTE: Obviously not ready for any serious use, more a showcase of how useful llama2 can be out of the box.  

# Installing

1. Uses ollama to host llama2 models for your platform (https://ollama.ai/) - dowbload and install appropriate version for your platform. 

2. Install requirements.txt

`pip install -r requirements.txt`

3. Run `streamlit run streamlit.py` to run the app. The first time you access it it may take a while as it downloads the appropriate model.





