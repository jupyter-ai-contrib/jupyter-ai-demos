# Jupyter AI Demos

This repo contains a set of demos for the new features of Jupyter AI v3 and associated projects.

## Jupyter Server Documents

- Jupyter Server Documents (JSD) is a new project that moves all document and kernel state to Jupyter Server using pycrdt
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
- Personas work with file attachments

## Personas as Python packages

https://github.com/jupyterlab/jupyter-ai/blob/main/packages/jupyter-ai/jupyter_ai/personas/base_persona.py

- Developers can build new personas as Python packages
- Any agentic AI framework is supported (LangGraph, CrewAI, Llama Index, Strands, etc.)
- All that is needed is to subclass `BasePersona`
- Can include a custom avatar for the AI persona
- Once installed, they are automatically enabled using entry points

## Local persona development

- Any Jupyter user can build local personas in a single `.py` file
- `.jupyter/personas/<persona_name>.py` files will be picked up dynamically
- Easy debugging in the chat documents
- Refresh local personas using `/refresh_personas`

## Tools

https://github.com/jupyter-ai-contrib/jupyter-ai-tools

- Tool calling is a key dimension of AI persona capabilities
- Jupyter will ship with a default set of tools
- Scope is similar to what Claude Code has
- These tools will edit files using the CRDTs for a full collaborative UX
- Still need to work on tool approval UX

## MCP

- Jupyter AI v3 will include built in support for MCP servers
- `.jupyter/mcp/config.json` for MCP server configuration, follows the standard format
- Jupyter AI will automatically start MCP servers and give clients to AI personas
- Needed to avoid MCP servers begin duplicated across different personas and chats

## Jupyternaut

- Jupyternaut will continue to be the default AI persona for Jupyter AI
- The default AI persona can also be configured in a config file
- Jupyternaut will ship with the default tools
- Goal is to be on par with Claude Code, et al. but with a Jupyter flavor

