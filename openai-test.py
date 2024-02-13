import openai

# Set your OpenAI API key here
openai.api_key = "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"

# Use the `openai.ChatCompletion.create` method directly without creating a `client` object
completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

# Print the message from the completion response
# Note: Adjust the response handling based on the actual structure of the completion response
print(completion.choices[0].message)
