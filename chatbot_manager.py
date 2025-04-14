from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

def convert_to_string(messages: list) -> str:
    converted_message: str = ""
    for message in messages:
        converted_message += f"{message['role']}: {message['content']}\n"

    return converted_message

def convert_to_string_etc(text) -> str:
    converted_text: str = ""
    for t in text:
        converted_text += f"{t}\n"
    return converted_text

def summerize_chat_messages(chat_history: str) -> str:
    template = """
    Your job is to summerize the chat history using 15 words or less without any newlines.

    History: {history}
    Output:

    """

    model = OllamaLLM(model="llama3.2",
                      max_new_tokens=1000,
                      )

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    summerization = chain.invoke({"history":chat_history})
    print(f"[+] (chatbot_manager) Chat history has been summerized: {summerization}")

    return summerization

def generate_personality(traits: tuple) -> str:
    template = """
    Keep your response concise. Use 40 words or less. Do not use new lines. Your job is to generate a personality and name based on the given traits.

    Traits: {traits}
    Output:

    """
    traits = convert_to_string_etc(traits)
    model = OllamaLLM(model="llama3.2",
                      max_new_tokens=1000
                      )
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    personality = chain.invoke({"traits":traits})
    print(f"[+] (chatbot_manager) Personality has been generated: {personality}")

    return personality

def save_history(chat_history: str) -> None:
    with open('ai_memories.txt', 'w') as file:
        file.write(chat_history)

def load_history(load_file: str) -> str:
    try:
        with open(load_file, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"[-] (chatbot_manager) Could not find find file {load_file}")
    except Exception as e:
        print(f"[-] (chatbot_manager) An exception happened {e}")

if __name__ == '__main__':
    history = '''
    Bob: Hello
    AI: hello! how may i assist you
    Bob: May you tell me the first 5 digits of pi
    AI: 3.14159
    Bob: Thanks
    '''
    traits = ('load', 'annoying', 'talkative', 'rough')

    output = summerize_chat_messages(history)
    personality = generate_personality(traits)  
