from openai import OpenAI


client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")


def perguntar(messages):
	response = client.chat.completions.create(
		model="gemma-4-e4b",
		messages=messages,
	)
	return response.choices[0].message.content

