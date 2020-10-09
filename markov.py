"""A Markov chain generator that can tweet random messages."""

import sys
from random import choice
import os
import discord
import secrets 


def open_and_read_file(filenames):
    """Take list of files. Open them, read them, and return one long string."""

    text_file = open(filenames)
    body = ''
    for filename in filenames:
        body = body + text_file.read()
        body = body.strip()
        
    text_file.close()

    return body


def make_chains(text_string):
    """Take input text as string; return dictionary of Markov chains."""

    chains = {}

    words = text_string.split(' ')
    words.append(None)
    for i in range(len(words) - 2):
        key = (words[i], words[i + 1])
        value = words[i + 2]

        if key not in chains:
            chains[key] = []

        chains[key].append(value)

    return chains


def make_text(chains, char_limit = None):
    """Take dictionary of Markov chains; return random text."""

    keys = list(chains.keys())
    key = choice(keys)
    word = choice(chains[key])

    words = [key[0], key[1]]
    while word is not None:
        # Keep looping until we have a key that isn't in the chains
        # (which would mean it was the end of our original text).
        if char_limit and len(' '.join(words)) > char_limit:
            break
        # Note that for long texts (like a full book), this might mean
        # it would run for a very long time.

        key = (key[1], word)
        words.append(word)                   
        word = choice(chains[key])  

    return ' '.join(words)


def randomness():
    text = open_and_read_file(choice(['gettysburg.txt', 'green-eggs.txt']))
    chains = make_chains(text)
    output_text = make_text(chains)
    return output_text


# Get the filenames from the user through a command line prompt, ex:
# python markov.py green-eggs.txt shakespeare.txt
# filenames = sys.argv[1:]


# Open the files and turn them into one long string
# text = open_and_read_file(filenames)

# Get a Markov chain
# chains = make_chains(text)

client = discord.Client()


@client.event
async def on_ready():
    print(f'Successfully connected! Logged in as {client.user}.')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$'):
        await message.channel.send(randomness())
    
    
token = os.environ['DISCORD_TOKEN']
client.run(token)
    


