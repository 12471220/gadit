import json

dic = {
    "name" : "张三",
    "age" : 20,
    "gender" : "male"
}

with open("src/test/dict.json", "w", encoding="GB2312") as f:
    json.dump(dic, f)