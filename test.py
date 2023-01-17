import os
import openai

openai.api_key = ""

response = openai.Completion.create(
  model="text-davinci-003",
  prompt="Describe Van Gogh's star moon night in 50 words",
  temperature=0.3,
  max_tokens=60,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0
)

print(response["choices"][0]["text"])