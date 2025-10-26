# Sistemas Inteligentes - Trabajo Final Integrador

Profesor: Dr. Pedro Araujo
Maestría en Ciencias de Datos
Facultad de Ingeniería - UCASAL
Alumno: Leopoldo Eugenio Lugones

## Caso de Estudio: Bitcoin Expert Assistant Chat Example using AutoGen

This script sets up a multi-agent chat system where a user can interact with a Bitcoin expert assistant.
The Bitcoin expert can fetch historical price data and instruct a plotting assistant to create visualizations.
The conversation continues until the user mentions "thank you" or a maximum number of turns is reached.
Required packages: autogen-agentchat, autogen-core, autogen-ext, yfinance, matplotlib, pandas, python-dotenv
Make sure to set the GEMINI_API_KEY environment variable for OpenAI access.

## Ejemplos

### <btc.py>

Implementa un equipo de agentes, para que un Usuario pueda interactuar con un Experto en Bitcoin (BitcoinExpert), Asistente de y un Asistente de Gráficos (PlotAssistant), permitiendo preguntas sobre Bitcoin y análisis de datos de precios. El Usuario deberá ingresar un rango de fechas (Desde, Hasta) para obtener el set de datos, mediante el cual se basará el mencionado análisis.

* Dataset: bitcoin.csv
* Plot: bitcoin_price_plot.png

### <btc_open_close.py>

Similar a <btc.py>, con la diferencia que agrega el set de datos las fechas de Apertura (Open) y Cierre (Close) del Bitcoin.

* Dataset: bitcoin_open_close.csv
* Plot: bitcoin_open_vs_close_plot.png

### Ejemplo de Ingreso Rango de Fechas

* **Start Date:** 2025-01-02
* **End Date:** 2025-10-20

## Pre-requisitos

Python 3.10 o superior

## IDE

Visual Studio Code
Plugins: Python, Pylance, Python Environment

## Instalación

* python -m venv .venv
* .venv\Scripts\activate.bat

* pip install -U "autogen-agentchat" "autogen-ext[openai]"
* pip install python-dotenv
* pip install yfinance
* pip install pandas
* pip install matplotlib

Instalación sugerida:
* pip install -r requirements.txt

## Referencias

[Autogen][def1]

[def1]: https://microsoft.github.io/autogen/stable/index.html

[AgentChat #][def2]

[def2]: https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/index.html
