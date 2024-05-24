import google.generativeai as genai

genai.configure(api_key="AIzaSyDC5rrrnwmiXGXKqGNfsl1RQVIOzl3RmBc")

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
]

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  safety_settings=safety_settings,
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "I'll give a list of weather conditions encountered by a flight after every 100km. Give the risk percentage of that route out of 100 and a sentence in the next line. Give a number in the first line as response and a sentence (key factors contributing to risk) in the next line, nothing else. You need to use lesser numbers for risk. Use 80 and above if situation is extremely bad like an accident. Use 20 - 40 if situation is slightly bad. 0 - 10 if situation is decent.",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Please provide the list of weather conditions encountered by the flight after every 100km. I'll then calculate the risk percentage and provide a sentence describing the key factors contributing to the risk. \n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "\nHeavily cloudy (overcast)\nHeavily cloudy (overcast)\nSlight rain showers\nHeavily cloudy (overcast)\nSlight rain showers\nSlight or moderate thunderstorm\nSlight or moderate thunderstorm\nSlight or moderate thunderstorm\nHeavily cloudy (overcast)\nSlight rain showers\nSlight or moderate thunderstorm\nHeavily cloudy (overcast)\nHeavily cloudy (overcast)\nHeavily cloudy (overcast)\nSlight or moderate thunderstorm\nSlight or moderate thunderstorm\nHeavily cloudy (overcast)\nHeavily cloudy (overcast)\nHeavily cloudy (overcast)\nFog\nHeavily cloudy (overcast)\nHeavily cloudy (overcast)\nHeavily cloudy (overcast)\nHeavily cloudy (overcast)\nHeavily cloudy (overcast)\nHeavily cloudy (overcast)\nHeavily cloudy (overcast)\nHeavily cloudy (overcast)",
      ],
    },
    {
      "role": "model",
      "parts": [
        "60\nThe combination of overcast conditions, rain showers, and thunderstorms throughout the route significantly increases the risk, especially with multiple instances of thunderstorms. \n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "Moderate drizzle\n\nFreezing rain light\n\nHeavy rain\n\nSnow grains\n\nPartly cloudy\n\nDepositing rime fog\n\nFreezing drizzle light\n\nDense drizzle\n\nSlight snow showers\n\nOvercast",
      ],
    },
    {
      "role": "model",
      "parts": [
        "40\nThe presence of freezing rain, snow grains, and depositing rime fog,",
      ],
    },
    {
      "role": "user",
      "parts": [
        "\nFreezing drizzle dense\n\nHeavy snow fall\n\nViolent rain showers\n\nMainly clear\n\nModerate rain\n\nFog\n\nSlight rain showers\n\nSlight or moderate thunderstorm\n\nSlight snow fall\n\nThunderstorm with heavy hail",
      ],
    },
    {
      "role": "model",
      "parts": [
        "70\nThe combination of heavy snowfall, violent rain showers, a thunderstorm with heavy hail, and dense freezing drizzle, \n",
      ],
    },
  ]
)

def get_risk_details(path_labels):
    input_text = ""
    for label in path_labels:
        input_text = input_text + "\n" + label
    response = chat_session.send_message(input_text)
    risk_percentage = int(response.text.splitlines()[0])
    risk_message = response.text.splitlines()[1]
    return [risk_percentage,risk_message]
