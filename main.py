'''
MAIN QUESTION: How did the Russians created a troll farm????

To do:
Add permanent memory?

'''
import random
import bsapi
import chatbot
bs = bsapi.Bsapi(pds_url = 'techywizwad.bsky.social',
                identifier = 'techywizwad.bsky.social',
)
ai = chatbot.AI()
topics = ('Explain how your day was', 'Explain what you did today', 'Explain the weather')

topic = random.choice(topics)
response = ai.chat(topic)

bs.post_stuff(response)
