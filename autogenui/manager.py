import json
import os
import autogen
import logging

# Configuration du logger
logging.basicConfig(level=logging.DEBUG)

class Manager(object):
    def __init__(self) -> None:
        self.config = self.load_config()
        self.messages = self.load_messages()

    def load_config(self) -> dict:
        try:
            logging.debug('WorkDir A : ' + os.getcwd())
            with open('/app/config/config.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            logging.error("Le fichier 'config.json' est introuvable.")
            return {}

    def load_messages(self) -> dict:
        try:
            logging.debug('WorkDir B : ' + os.getcwd())
            with open('/app/config/messages.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            logging.error("Le fichier 'messages.json' est introuvable.")
            return {}

    def run_flow(self, prompt: str, flow: str = "default") -> None:
        logging.debug('WorkDir : ' + os.getcwd())
        llm_config = self.config.get('llm_config', {})
        llm_config['config_list'][0]['api_key'] = os.getenv('OPENAI_API_KEY')

        assistant = autogen.AssistantAgent(
            name="assistant",
            system_message=self.messages.get('assistant_system_message', ''),
            llm_config=llm_config,
        )

        user_proxy_config = self.config.get('user_proxy_config', {})
        user_proxy_config['llm_config'] = llm_config
        termination_msg = user_proxy_config.get('is_termination_msg', '')
        user_proxy_config['is_termination_msg'] = lambda x: x.get("content", "").rstrip().endswith(termination_msg)

        user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            **user_proxy_config
        )

        user_proxy.initiate_chat(
            assistant,
            message=prompt,
        )

        messages = user_proxy.chat_messages[assistant]
        return messages
