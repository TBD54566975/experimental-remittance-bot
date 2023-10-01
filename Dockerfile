FROM ollama/ollama

RUN /bin/ollama serve --help
#RUN ollama pull llama