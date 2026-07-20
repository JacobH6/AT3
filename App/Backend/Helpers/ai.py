from openai import OpenAI
import os
from Backend.utils.constants import *
from dotenv import load_dotenv
from time import sleep


load_dotenv(
    os.path.join(BASE_DIR, ".env")
)

bugetary_reasons=True

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def ask_ai(prompt):

    if bugetary_reasons==True:
        return "The Ai is unavalible at the moment"

        ##For developers. WHO THE HELL SPENT $900 ON TOKENS!!!!??!?!?!

    response = client.responses.create(

        model="gpt-5-mini",

        input=prompt

    )

    return response.output_text