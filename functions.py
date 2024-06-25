import openai
import settings as s

openai.api_key = s.openai_api_key

# OpenAI API for chat completion:
# https://platform.openai.com/docs/api-reference/chat/create?lang=python
def chat_completion(_prompt):
    response = openai.chat.completions.create(
        model=s.gpt_model,
        messages=_prompt,
    )

    output = response.choices[0].message.content
    return output


# OpenAI API for generating text embeddings:
# https://platform.openai.com/docs/api-reference/embeddings/create
def text_embedding(_text):
    response = openai.embeddings.create(
        model=s.embedding_model,
        input=_text,
    )

    output = response.data[0].embedding
    return output
