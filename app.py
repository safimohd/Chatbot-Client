# app.py
import chainlit as cl

@cl.on_chat_start
async def start():
    await cl.Message(content="Hello! Welcome to my Chainlit app.").send()

@cl.on_message
async def main(message: cl.Message):
    user_input = message.content
    reply = f"You said: {user_input}"
    await cl.Message(content=reply).send()