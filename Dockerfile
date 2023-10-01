FROM ollama/ollama

ENTRYPOINT ["/bin/ollama"]
CMD ["serve"]