# Remittance risk flagging app

*Experimental* showcase of llama2 pre-trained open source models. 

This app uses llama2 to show a ChatGPT competitive LLM to score remittance descriptions. Ie a human explains what they are transferring funds for and it comes up with a High,Low or Med score and reason for flagging for a further screening perhaps by another human (or to apply other rules). 

Uses <a href="https://ai.meta.com/llama/">llama2</a> model (7b also works ok) so it can run on modest hardware. 

NOTE: Obviously not ready for any production use, more a showcase of how useful llama2 can be out of the box. 

![Screenshot 2023-10-02 at 8 58 56 am](https://github.com/TBD54566975/experimental-remittance-bot/assets/14976/46ead9b7-21aa-4325-b63b-060520011cb7)

![Screenshot 2023-10-02 at 8 59 15 am](https://github.com/TBD54566975/experimental-remittance-bot/assets/14976/754715d1-fc05-4dda-b344-23fdce21e0d6)

# Installing

1. This uses ollama to host llama2 models for your platform (https://ollama.ai/) - dowbload and install appropriate version for your platform. 

eg on linux you can run: `docker run -p 11434:11434 ollama/ollama`
on macos `ollama serve` (or run the application)

2. Install requirements.txt

`pip install -r requirements.txt`

3. Run `streamlit run streamlit.py` to run the app. The first time you access it it may take a while as it downloads the appropriate model. You can set OLLAMA_HOST to point to `hostname:port` for the ollama server.





