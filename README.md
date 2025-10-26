# Bitcoin Expert Assistant Chat Example using AutoGen

This script sets up a multi-agent chat system where a user can interact with a Bitcoin expert assistant.
The Bitcoin expert can fetch historical price data and instruct a plotting assistant to create visualizations.
The conversation continues until the user mentions "thank you" or a maximum number of turns is reached.
Required packages: autogen-agentchat, autogen-core, autogen-ext, yfinance, matplotlib, pandas, python-dotenv
Make sure to set the GEMINI_API_KEY environment variable for OpenAI access.
