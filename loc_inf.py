# script to run and send messages to the local model and get responses
import os
from rich import print
from llama_cpp import Llama
from typing_extensions import TypedDict, Literal
from typing import List

Role = Literal["system", "user", "assistant"]


class Message(TypedDict):
    role: Role
    content: str


B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
DEFAULT_SYSTEM_PROMPT = """\
You are a Windows computer with the ability to run any code you want, if you are given a task you will do all you can to achieve that task. when you are given a prompt return a response with a plan of what code you want to run. You should start your response with a plan, The commands you provide should be in a single code block encapsulated in '''python and ''' for Python and should be valid Python programs written in an optimal way with the intent of getting the best result."""


def make_prompt_llama2(llm, messages: List[Message]) -> List[int]:
    if messages[0]["role"] != "system":
        messages = [
            {
                "role": "system",
                "content": DEFAULT_SYSTEM_PROMPT,
            }
        ] + messages

    messages = [
        {
            "role": messages[1]["role"],
            "content": B_SYS + messages[0]["content"] + E_SYS + messages[1]["content"],
        }
    ] + messages[2:]

    assert all([msg["role"] == "user" for msg in messages[::2]]) and all(
        [msg["role"] == "assistant" for msg in messages[1::2]]
    ), (
        "model only supports 'system', 'user' and 'assistant' roles, "
        "starting with 'system', then 'user' and alternating (u/a/u/a/u...)"
    )

    dialog_tokens = sum(
        [
            llm.tokenize(
                bytes(
                    f"{B_INST} {(prompt['content']).strip()} {E_INST} {(answer['content']).strip()} ",
                    "utf-8",
                ),
                add_bos=True,
            )
            + [llm.token_eos()]
            for prompt, answer in zip(
                messages[::2],
                messages[1::2],
            )
        ],
        [],
    )

    assert messages[-1]["role"] == "user", f"Last message must be from user, got {messages[-1]['role']}"

    dialog_tokens += llm.tokenize(
        bytes(
            f"{B_INST} {(messages[-1]['content']).strip()} {E_INST}", "utf-8"),
        add_bos=True,
    )

    return dialog_tokens


class LLMChatBot:
    def __init__(self, model_path):
        if not os.path.exists(model_path):
            print("Model not found at the specified path.")
            return

        self.llama = Llama(model_path=model_path, n_ctx=1024, n_gpu_layers=-1)
        print("Local LLM loaded successfully.")

    def get_response(self, user_message):
        messages: List[Message] = [
            Message(role="user", content=user_message),
        ]

        tokens = make_prompt_llama2(self.llama, messages)

        completion = self.llama.generate(tokens=tokens, temp=0.01)

        response_text = ""

        for token in completion:
            if token == self.llama.token_eos():
                break
            response_text += self.llama.detokenize([token]).decode("utf-8")

        return response_text


if __name__ == "__main__":
    # instantiate the chatbot
    bot = LLMChatBot(
        r'C:\Users\Jeff\AppData\Local\Open Interpreter\Open Interpreter\models\codellama-7b-instruct.Q3_K_S.gguf')

    while True:
        user_message = input("You: ")
        response = bot.get_response(user_message)
        print("LLM: " + response)
