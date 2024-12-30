import discord
import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the tokens
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")  # Discord bot token
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # OpenAI API key

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

# Initialize global chat variable
chat = ""


# Define a custom Discord client
class MyClient(discord.Client):

    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_message(self, message):
        global chat
        try:
            # Append messages to chat log
            chat += f"{message.author}: {message.content}\n"
            print(f'Message from {message.author}: {message.content}')

            # Ignore messages from the bot itself
            if self.user != message.author:
                # Check if the bot is mentioned
                if self.user in message.mentions:
                    response = openai.ChatCompletion.create(
                        model=
                        "gpt-3.5-turbo",  # Use the newer ChatCompletion API
                        messages=[{
                            "role":
                            "system",
                            "content":
                            "You are HardkAI, a helpful assistant."
                        }, {
                            "role": "user",
                            "content": chat
                        }],
                        temperature=1,
                        max_tokens=256,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0)
                    # Extract and send the response
                    channel = message.channel
                    message_to_send = response['choices'][0]['message'][
                        'content'].strip()
                    await channel.send(message_to_send)
        except Exception as e:
            print(f"Error: {e}")
            chat = ""


# Set Discord intents
intents = discord.Intents.default()
intents.message_content = True

# Initialize the client with intents
client = MyClient(intents=intents)

# Run the bot
client.run(DISCORD_TOKEN)
