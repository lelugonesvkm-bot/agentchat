# btc.py
# Bitcoin Expert Assistant Chat Example using AutoGen
#
# An example of using AutoGen to create a group chat between a Bitcoin expert assistant and a user.
# The user can ask questions about Bitcoin, and the assistant provides detailed answers.
# The chat continues until the user mentions "thank you" in their message.
# The conversation is displayed in the console.
# Additional imports for Bitcoin data fetching and plotting

# Import necessary modules
import os
import asyncio
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core.tools import FunctionTool
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv

# Ensure required packages are installed
# pip install yfinance matplotlib pandas

# Load environment variables    
load_dotenv()

# Initialize the model client
model_client = OpenAIChatCompletionClient(
    model="gemini-2.0-flash",
    api_key=os.getenv("GEMINI_API_KEY"),
    )

# Define a tool to fetch Bitcoin price data
def fetch_bitcoin_data(start_date: str, end_date: str) -> str:
    """
    Fetch historical Bitcoin price data between two dates and save it to a CSV file.
    :param start_date: The start date for fetching data (YYYY-MM-DD).
    :param end_date: The end date for fetching data (YYYY-MM-DD).
    :return: The filename of the saved CSV file.
    """

    # Import yfinance for data fetching
    import yfinance as yf

    # Download historical Bitcoin data using yfinance
    btc_data = yf.download('BTC-USD', start=start_date, end=end_date,)
    
    # Save the data to a CSV file
    btc_data = btc_data.reset_index()
    data_to_save = btc_data[['Date', 'Open', 'Close']]
    filename = "bitcoin_data_open_close.csv"
    data_to_save.to_csv(filename, index=False)

    return filename

# Define a function to plot Bitcoin price data
def plot_bitcoin_data(filename: str) -> str:
    """
    Plot Bitcoin price data (Open vs. Close) from a CSV file and save the plot as a PNG file.
    :param filename: The CSV file containing Bitcoin price data (must include 'Date', 'Open', and 'Close').
    :return: The filename of the saved PNG plot.
    """
    
    # Import necessary libraries for plotting
    import pandas as pd
    import matplotlib.pyplot as plt

    # Use a non-interactive backend for matplotlib
    # Esto es crucial para entornos de agentes
    try:
        plt.switch_backend('Agg')
    except Exception:
        # Esto maneja el caso donde el backend ya está configurado (como en la corrección global)
        pass 
    
    try:
        # 1. Read data from the CSV file (REQUIERE que el CSV tenga las columnas 'Open' y 'Close')
        data = pd.read_csv(filename, parse_dates=['Date'])
        
        # Validación básica para asegurar que las columnas existen
        if 'Open' not in data.columns or 'Close' not in data.columns:
             raise ValueError("El archivo CSV debe contener las columnas 'Open' y 'Close' para la comparación.")
            
        # 2. Create the chart
        plt.figure(figsize=(12, 6))
        
        # Graficar Precio de Cierre (Close)
        plt.plot(data['Date'], data['Close'], label='Precio de Cierre (Close)', color='red', linewidth=2)
        
        # Graficar Precio de Apertura (Open)
        plt.plot(data['Date'], data['Open'], label='Precio de Apertura (Open)', color='blue', linestyle='--', linewidth=1.5)
        
        plt.title('Bitcoin: Comparativa de Precios de Apertura y Cierre', fontsize=16)
        plt.xlabel('Fecha', fontsize=12)
        plt.ylabel('Precio (USD)', fontsize=12)
        
        # Mostrar ambas leyendas
        plt.legend(loc='best', fontsize=10) 
        plt.grid(True, linestyle=':', alpha=0.6)
        
        # 3. Save the chart as a PNG file
        output_filename = "bitcoin_open_vs_close_plot.png"
        plt.savefig(output_filename) 
        
        # Close the figure to free memory    
        plt.close() 
        
        return f"✅ Gráfico de comparativa Open/Close generado y guardado exitosamente como '{output_filename}'." 
    
    except Exception as e:
        # Asegurarse de cerrar figuras pendientes si hay un error
        plt.close() 
        return f"❌ Error al generar o guardar el gráfico: {e}"     

# Define the FunctionTool for fetching Bitcoin data 
bitcoin_tool = FunctionTool(
    func=fetch_bitcoin_data, description="Fetch Bitcoin price data between two dates and save to CSV."    
)

# Tool for plotting Bitcoin data
plot_tool = FunctionTool(
    func=plot_bitcoin_data, description="Plot Bitcoin price data from a CSV file."
)

# Agents definitions

# Create the Bitcoin expert assistant agent  
bitcoin_expert = AssistantAgent(
    name="BitcoinExpert",
    model_client=model_client,
    tools=[bitcoin_tool],
    system_message=(
        "You are a Bitcoin expert assistant. You can provide detailed information about Bitcoin, "
        "including its history, technology, market trends, and investment strategies. "
        "You can also use the provided tool to fetch historical Bitcoin price data for analysis. "
        "Always provide thorough and accurate answers to the user's questions. "
        "If the user requests data analysis, use the tool to fetch the data and then analyze it. "
        "Inform the user about the data you have fetched and your analysis. "
        "Inform the user when the file csv is ready for analysis. "
        "Make sure to explain your analysis clearly. "
        "Do not generate plots yourself; instead, instruct the PlotAssistant to create them using the data you provide. "
        "Inform the user when the plot is ready to be viewed. "
        "If the user mentions 'thank you', conclude the conversation politely."
    ),
)

# Create the Plot assistant agent
plot_assistant = AssistantAgent(
    name="PlotAssistant",
    model_client=model_client,
    tools=[plot_tool],
    system_message=(
        "You are a plotting assistant. Your role is to create visualizations based on the data provided by the Bitcoin expert. "
        "When the Bitcoin expert provides a CSV file with Bitcoin price data, generate a plot of the price trends over time. "
        "Ensure that the plots are clear and well-labeled. "
        "Once you have created the plot, inform the Bitcoin expert so they can share it with the user."
        "If the user mentions 'thank you', conclude the conversation politely."
    ),
)

# Create the user proxy agent
user_proxy = UserProxyAgent(
    name="User",
    description="A user interested in learning about Bitcoin and its market trends.",    
)

# Set up the group chat team
team = RoundRobinGroupChat(
    participants=[user_proxy, bitcoin_expert, plot_assistant],
    termination_condition=TextMentionTermination("thank you"),
    max_turns=10,
)

# Function to orchestrate the chat
async def orchestrate_chat(team, task):
    async for msg in team.run_stream(task=task):
        if isinstance(msg, TextMessage):
            print(message:=f'{msg.source}: {msg.content}')
        elif isinstance(msg, TaskResult):
            print(message:=f'Stop reason: {msg.stop_reason}')

# Main function to run the chat
async def main():
    task = "I would like to learn about Bitcoin. Can you provide an overview and analyze its price trends over the last year?"
    await orchestrate_chat(team, task)
if __name__ == '__main__':
    asyncio.run(main())
