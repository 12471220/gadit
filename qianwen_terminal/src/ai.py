import json
import dashscope as ds
import time
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
                self.save_messages()
                print("total token:", self.token_count)
                print("total cost (less than):", self.token_cost(self.token_count))
                break
    

    def user_input(self):
        all_input = ""
        flag = 0
        while True:
            try:
                if flag == 0:
                    msg = input(">>> ")
                else:
                    msg = input("... ")

                if msg == "" or msg[-1] != "\\":
                    all_input += msg
                    break
                all_input += msg[:-1] + "\n"
                flag = 1
            except KeyboardInterrupt:
                raise KeyboardInterrupt

        print("\033[32m" + all_input + "\033[0m")
        self.messages.append({"role": "user", "content": all_input})
    
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
                    print('error code:',chunk.status_code,"\nerror message:", chunk.message)
        else:
            if response.status_code == HTTPStatus.OK:
                msg_content = response.output.choices[0].message.content
                self.messages.append({"role": "assistant", "content": msg_content})
                self.token_count += response.usage.total_tokens

                print(msg_content)
            else:
                print('error code:', response.status_code,"\nerror message:", response.message)

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
            case "qwen-max-longcontext":
                return num/1000 * 0.12
            
    def save_messages(self):
        print("\nwait, saving messages...")
        filename = self.summerize(self.messages)
        with open(f"messages/{filename}.json", "w", encoding="utf-8") as f:
            json.dump(self.messages, f, indent=2, ensure_ascii=False)


    def summerize(self, msg:list[dict]):
        response = ds.Generation.call(
            api_key=self.apikey,
            model=self.model,
            messages=[
                *msg,
                {"role": "user", "content": "请精简总结以上对话内容, 10字以内"},
            ],
            result_format='message'
        )
        if response.status_code == HTTPStatus.OK:
            return response.output.choices[0].message.content
        else:
            print('\nsummerize error:', Exception(response.status_code, response.message))
            return "cant_summerize"+time.strftime('%Y-%m-%d_%H-%M-%S')
    
