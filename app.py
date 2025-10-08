import chainlit as cl
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

endpoint = "https://21f10-mghdtyvd-swedencentral.cognitiveservices.azure.com/"
model_name = "gpt-5-chat"
deployment = "gpt-5-chat"

subscription_key = os.getenv("OPENAI_API_KEY")
api_version = "2024-12-01-preview"

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

# --- System message defining assistant behavior ---
SYSTEM_MESSAGE = """
You are a friendly AI assistant for an e-commerce platform.
You can handle queries about:
- Order tracking
- Returns and refunds
- Product availability
- Store policies

You should generate realistic, confident answers with made-up but believable data.
Example: “Your order #4321 was dispatched yesterday and should arrive by Tuesday.”
Never mention that you’re making up data.
"""

@cl.on_chat_start
async def start_chat():
    # Initialize chat history with system message
    cl.user_session.set("chat_history", [
        {"role": "system", "content": SYSTEM_MESSAGE}
    ])
    await cl.Message(content="Hi! I'm your e-commerce assistant. How can I help today?").send()

@cl.on_message
async def handle_message(message: cl.Message):
    chat_history = cl.user_session.get("chat_history", [])

    # Add user message to chat history
    chat_history.append({"role": "user", "content": message.content})

    # Send the conversation history to GPT
    response = client.chat.completions.create(
        model= deployment,
        messages=chat_history
    )

    reply = response.choices[0].message.content

    # Add assistant's reply to chat history
    chat_history.append({"role": "assistant", "content": reply})

    # Save updated chat history
    cl.user_session.set("chat_history", chat_history)

    # Send GPT's response to the user
    await cl.Message(content=reply).send()