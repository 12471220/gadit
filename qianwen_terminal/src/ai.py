import json
import dashscope as ds
from http import HTTPStatus

class Ali_AI:
    def __init__(self):
        with open("src/env.json", "r") as f:
            env = json.load(f)

        self.apikey = env["apikey"]
        self.model = env["model"]
        self.endpoint = env["endpoint"]
        self.stream = env["stream"]
        self.messages: list[dict] = []
        self.token_count = 0
    
    def long_chat(self):
        while True:
            try:
                res = self.single_chat()
                self.messages.append({"role": "assistant", "content": res})

            except KeyboardInterrupt:
                print("\ntotal token:", self.token_count)
                print("total cost (less than):", self.token_cost(self.token_count))
                break
    

    def user_input(self):
        msg = input("usr:")
        self.messages.append({"role": "user", "content": msg})
    
    def single_chat(self):
        self.user_input()

        response = ds.Generation.call(
            api_key=self.apikey,
            model=self.model,
            stream=self.stream,
            incremental_output=self.stream,
            messages=self.messages,
            result_format='message',
        )

        if self.stream:
            msg_content = ""
            for chunk in response:
                if chunk.status_code == HTTPStatus.OK:
                    msg_content += chunk.output.choices[0].message.content
                    print(chunk.output.choices[0].message.content, end="", flush=True)

                    if chunk.output.choices[0].finish_reason == "stop":
                        self.token_count += chunk.usage.total_tokens
                        break
                else:
                    raise Exception(chunk.status_code, chunk.body)
        else:
            if response.status_code == HTTPStatus.OK:
                msg_content = response.output.choices[0].message.content
                self.messages.append({"role": "assistant", "content": msg_content})
                self.token_count += response.usage.total_tokens

                print(f"assistant: {msg_content}")
            else:
                raise Exception(response.status_code, response.body)

        print('\n')
        return msg_content

    def token_cost(self, num:int):
        match self.model:
            case "qwen-long":
                return num/1000 * 0.002
            case "qwen-turbo":
                return num/1000 * 0.0006
            case "qwen-plus":
                return num/1000 * 0.002
            case "qwen-max":
                return num/1000 * 0.06
            


    def chat_test(self):
        response = ds.Generation.call(
            api_key=self.apikey,
            model=self.model,
            messages=[
                {"role": "user", "content": "你好"}
            ],
            result_format='message'
        )
        print(json.dumps(response, indent=2))
        print(response.output.choices[0].message.content)
    