FROM ollama/ollama

# Start the ollama server in the background, wait, then run your command
RUN /bin/ollama serve & sleep 10 && ollama pull llama2

ENTRYPOINT ["/bin/ollama"]
CMD ["serve"]