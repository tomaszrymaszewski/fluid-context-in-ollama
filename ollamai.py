def ai(name: str, mood: str = "interested", model: str = "llama3.2", ans_length: str = "short"):
    import requests
    from ollama import chat
    from datetime import datetime
    import json
    from urllib.request import urlopen
    import pywhatkit

    # Get date & time
    date = datetime.today().strftime('%d.%m.%Y')

    day_of_week = datetime(int(date.split(".")[2]), int(date.split(".")[1]), int(date.split(".")[0])).isoweekday()
    weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    time = datetime.today().strftime('%H:%M')

    # Get location
    location = json.load(urlopen("http://ipinfo.io/json"))
    city = location['city']
    country = location['country']
    timezone = location['timezone']

    # Get weather (only activated when "temperature" or "weather" included in input because of API credits)
    def get_weather():
        api_key = 'e54ae857b9a4036e7444de2230356239'
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={api_key}&units=metric'
        response = requests.get(url)
        data = response.json()

        if 'main' in data and 'temp' in data['main']:
            temp = data['main']['temp']
            condition = data['weather'][0]['description']
            temp_min = data['main']['temp_min']
            temp_max = data['main']['temp_max']
            pressure = data['main']['pressure']
            humidity = data['main']['humidity']
        else:
            print("Temperature information not available.")

        return temp, condition, temp_min, temp_max, pressure, humidity

    # Contexts
    description_context = f"You are an assistant. Your name is {name}. Only give answers of {ans_length} length. You aren't from any specific location and you don't have any relatives. Don't use emojis in your answers."
    ip_context = f"This is the user is located in {city}, {country}. Today is {day_of_week}, {date}. It is currently {time} ({timezone} time). "
    mood_context = "In your responses sound " + mood
    messages = [
        {
            "role": "system",
            "content": description_context,
        },
        {
            "role": "system",
            "content": ip_context,
        },
        {
            "role": "system",
            "content": mood_context,
        }
    ]

    def remove_unwanted(message):
        return message.replace("\n", " ").replace("**", "").replace("`", "")

    def working_on_it(json):
        print("Working on it...")
        if json["function"] == "play":
            pywhatkit.playonyt(str(json["info"]))
            return f"Playing {json['info']}..."
        if json["function"] == "calculate":
            print(f"Calculating {json['info']}...")


    while True:
        prompt = input("YOU: ")

        # variable for context of given function
        global function_used

        # Play song function
        if "play" in prompt:
            print("I'm working on playing that...")
            PLAY_SONG = ("Only if the user says that they want to play or stream a song or tune, output a json with "
                         "structure: {\"function\": \"play\", \"info\":\"song name\"}. Never mention the artist name "
                         "even if it is provided. Only if the user wants to play a song, solely output the json - no "
                         "additional comments or notes. If the user uses the word play in a different context and "
                         "wants to e.g. ask about a player, dont provide the json.")
            function_used = {"role": "system", "content": PLAY_SONG}

        # Weather function
        elif "weather" in prompt or "temperature" in prompt or "humidity" in prompt or "pressure" in prompt:
            print("<weather function used>")
            temp, condition, temp_min, temp_max, pressure, humidity = get_weather()
            GET_WEATHER = (
                f"In {city}, the temperature is {round(temp)}, condition is {condition}, lowest temperature today is {round(temp_min)}, highest temperature today is {round(temp_max)}, pressure is {pressure}, humidity is {humidity}. "
                "Always use the metric system. Only give this data when the user wants to learn the weather at their location. When you do give it, give a cohesive description.")
            function_used = {"role": "system", "content": GET_WEATHER}

        # Calculate function
        elif "calculate" in prompt or "1" in prompt or "2" in prompt or "3" in prompt or "4" in prompt or "5" in prompt or "6" in prompt or "7" in prompt or "8" in prompt or "9" in prompt:
            print("<calculate function used>")
            CALCULATE = (f"Only if the user says that they want to calculate an equation, solely output a json with "
                         "structure: {\"function\": \"calculate\", \"info\":\"equation using operators +, -, =, ^, "
                         "sqrt, *, /\"}. ")
            function_used = {"role": "system", "content": CALCULATE}

        else:
            function_used = {"role": "system", "content": ""}

        messages.append(function_used)

        if "thank you" == prompt or "bye" == prompt or "quit" == prompt:
            break

        messages.append({"role": "user", "content": prompt})

        #try:
        response = chat(model=model, messages=messages, stream=False)

        message = remove_unwanted(response['message']['content'])
        # print("Message content:", message)  # Add this line for debugging
        if "{" in message:
            # Extracting the content within '{' and '}'
            start_index = message.find('{')
            end_index = message.find('}')
            extracted_content = message[start_index:end_index + 1]

            loaded_json = json.loads(extracted_content)
            message = working_on_it(loaded_json)

        if function_used:
            messages.remove(function_used)

        messages.append(response['message'])

        # print(messages)  # For testing

        print(name.upper() + ": " + message)
        # return name.upper() + ": " + message

        #except Exception as e:
        #    print(f"An error occurred: {e}")
