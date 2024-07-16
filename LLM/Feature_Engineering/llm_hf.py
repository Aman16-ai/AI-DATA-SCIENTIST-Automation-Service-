from hugchat import hugchat
from hugchat.login import Login
from dotenv import load_dotenv
import os

load_dotenv()
# Login huggingface
# email = os.getenv("hf_email")
# passwd = os.getenv("hf_passwd")


class llm_class:
    def __init__(self, email, passwd):
        self.email = email
        self.passwd = passwd
        try:
            sign = Login(email, passwd)
            cookies = sign.login()
            self.chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
            # self.chatbot.switch_llm(3) # for mistral 8*7B
            # self.chatbot.switch_llm(2) # for hfH4
            self.chatbot.switch_llm(5) # for gemma
        except Exception as e:
            print("Invalid credentials huggingchat", e)

    def ask(self, prompt):
        res = self.chatbot.query(prompt)
        return res["text"] or ""

# llm = llm_class(os.getenv("hf_email"),os.getenv("hf_passwd"))
# print(llm.ask("What is machine learning"))