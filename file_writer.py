from json import dumps
import json

FILE_PATH = "./output.jsonl"

class FileWriter:
    def save(self, content):
        with open(FILE_PATH, "w") as file:
            for text in content:
                json_text = json.dumps(text)
                file.write(f"{json_text}\n")
