import json

with open('src/env.json', 'r') as f:
    env = json.load(f)

# load加载成字典
print(env)
print(type(env))