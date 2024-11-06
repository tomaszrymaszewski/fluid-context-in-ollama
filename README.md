# AI Assistant

This project defines an AI-powered assistant function ai() that responds based on user input, with specific features for playing music, retrieving weather information, and performing calculations. The assistant’s behavior can be tailored by modifying its name, mood, response length, and model version.

## Features

* Real-time Information: Provides location-based information (city, country, timezone) and retrieves the current date and time.
* Weather Data: Fetches weather conditions like temperature, humidity, and pressure when prompted.
* Current date, time and location: Uses the IP address and the datetime python library to access your information to be more helpful.
* Calculation: Evaluates and returns answers for basic arithmetic and mathematical operations.
* Flexible Behavior: Allows customization of assistant's name, mood, model, and response length.

## Installation

1. Clone the repository: \
```git clone https://github.com/tomaszrymaszewski/fluid-context-in-ollama```
2. Install required packages: \
```pip install requests ollama pywhatkit urllib```
3. Download Ollama: \
- go to https://ollama.com and download the Ollama app
- open the terminal and run ```ollama run <model name>``` (default: ```ollama run llama3.2```)
4. Weather API Key: 
Replace api_key in get_weather() with a valid OpenWeatherMap API key.

## Usage

1. Run ```python main.py```
2. After ```YOU: ``` appears just type the question/request

## Function Parameters

| Parameter   | Type | Default Value | Description                                           |
|-------------|------|---------------|-------------------------------------------------------|
| `name`      | str  | `"Kai"`       | The name of the assistant.                            |
| `mood`      | str  | `"interested"`| Adjusts the assistant's tone, e.g., "happy" or "serious". |
| `model`     | str  | `"llama3.2"`  | AI model to use for responses.                        |
| `ans_length`| str  | `"short"`     | Controls the length of the assistant’s responses.     |
