
# import openai, tenacity

import os
import openai
openai.api_key = "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"

poem = "阮郎"

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
      {"role": "system", "content": "You are a reviewer in the field of chinese classical poetry and you need to critically review this article"},  # chatgpt 角色
      {"role": "assistant",
       "content": "This is the <Answer> part of an English document, where I need your help to read and summarize the following questions." },
      {"role": "user", "content": f"""                 
                       Allusions refer to the ancient stories and words quoted in poems and texts.
                       1. What is the meaning of {poem}? (Answer only the allusion word)
                       
                       Follow the format of the output that follows:                  
                       1. Allusions: xxx\n\n
                       2. Background and meaning: xxx\n\n
                       
                       Be sure to statements as concise and academic as possible, do not have too much repetitive information, numerical values using the original numbers, be sure to strictly follow the format, the corresponding content output to xxx, in accordance with \n line feed.                 
                       """},

      # {"role": "user", "content": "Tell the world about the ChatGPT API in the style of a pirate."}
  ]
)

print(completion.choices[0].message.content)

