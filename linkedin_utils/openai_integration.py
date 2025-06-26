import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_linkedin_comment(
    post_text, agent_history=None, model="gpt-3.5-turbo", temperature=0.7
):
    """
    Generate a comment for a LinkedIn post using the post context and agent history.
    :param post_text: Text of the LinkedIn post
    :param agent_history: List of strings with the agent's interaction history
    :param model: OpenAI model to use
    :param temperature: Response temperature
    :return: Suggested comment string
    """
    messages = []
    if agent_history:
        for hist in agent_history:
            messages.append({"role": "system", "content": hist})
    messages.append({
        "role": "user",
        "content": f"Reply in a professional and engaging way to the following LinkedIn post: {post_text}",
    })

    response = client.chat.completions.create(
        model=model, messages=messages, temperature=temperature, max_tokens=120
    )
    return response.choices[0].message.content.strip()
