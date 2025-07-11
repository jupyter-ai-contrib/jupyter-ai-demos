# Jupyter AI Demos

This repo contains a set of demos for the new features of Jupyter AI v3 and associated projects.

# Demo B

## Foundations of Jupyter Server Documents

- JSD is a new project that moves all document and kernel state to Jupyter Server using pycrdt
- Lightening fast document updates
- Low memory usage
- All documents are autosaved by default
- Robust handling for out of band changes on text files and notebooks

## Chat files 

https://github.com/jupyterlab/jupyter-chat

- Chat files are now a core document type for JupyterLab
- These collaborative chat files enable human/human and human/ai collaboration
- You can organize you chat files on the file system
- The left panel offers a leightweight chat experience
- The launcher and main area offer a full document oriented chat experience
- Jupyter chat supports file attachments through drag and drop

## Jupyter AI

https://github.com/jupyterlab/jupyter-ai

- In Jupyter AI v3, everything is an AI persona
- Simply @ mention an AI person to collaborate with it
- Jupyternaut is the default, and the last mentioned persona is sticky for lightweight threads
- Each chat file will find the nearest `.jupyter` directory and use it for configuration
- `.jupyter/mcp/config.json` for MCP server configuration
- `.jupyter/personas/<name>_persona.py` for additional AI personas
