import chatbot_manager
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

class AI:

    def __init__(self, *personality: str, long_mem_leng: int = 10 ):
        self.long_mem_leng: int = long_mem_leng
         
        self.generate_personality = chatbot_manager.generate_personality(personality)

        self.template = '''
        Limit your responses to 25 words or less. What you say must be on a single line. Act like you are posting on twitter. {personality} 

        Summerized Context: {context_short}

        Here is the conversaion history: {context}

        Question: {question}

        Answer:
        
        '''

        self.context: list = []
        self.context_short: list = [] 

        self.model = OllamaLLM(model="llama3.2",
                        max_new_tokens=2000,
                        temperature=1.3)

        self.prompt = ChatPromptTemplate.from_template(self.template)
        self.chain = self.prompt | self.model

    def chat(self, message: str) -> str:
        history: str = chatbot_manager.convert_to_string(self.context) 

        if len(self.context) > self.long_mem_leng:
            memory: str = chatbot_manager.summerize_chat_messages(history)
            self.context_short.append(memory)
            self.context.clear()

        summeries: str = chatbot_manager.convert_to_string_etc(self.context_short)

        self.context.append({'role':'user', 'content':f'{message}'})
        ai_message: str = self.chain.invoke({"question":message, 
                                             "context":history, 
                                             "context_short":summeries,
                                             "personality":self.generate_personality})
        self.context.append({'role':f'assistant', 'content':f'{ai_message}'})
        print("[+] (AI) Chatbot has responded")
        return ai_message


if __name__ == '__main__':
    bot = AI()
    while True:
        user_message = input('[I] User >> ')
        response = bot.chat(user_message)
        print(f"[+] AI ~> {response}")
