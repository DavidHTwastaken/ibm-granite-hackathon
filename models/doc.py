import requests
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import time

def generate_doc(project):
    start_load_models = time.time()
    device = "cpu"  # or "cpu"
    # "ibm-granite/granite-8b-code-instruct-4k"
    model_path = 'ibm-granite/granite-3b-code-instruct-2k'
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    # drop device_map if running on CPU
    model = AutoModelForCausalLM.from_pretrained(model_path)
    model.eval()
    time_load_models = time.time() - start_load_models
    start_gen = time.time()
    # change input text as desired
    chat = [
        {"role": "user", 
        "content": f'Create a markdown document explaining the following project. \
            I will provide the file paths followed by their content. Here is the project:\n {project}'},
    ]
    chat = tokenizer.apply_chat_template(
        chat, tokenize=False, add_generation_prompt=True)
    # tokenize the text
    input_tokens = tokenizer(chat, return_tensors="pt")
    # transfer tokenized inputs to the device
    for i in input_tokens:
        input_tokens[i] = input_tokens[i].to(device)
    # generate output tokens
    output = model.generate(**input_tokens, max_new_tokens=100)
    # decode output tokens into text
    output = tokenizer.batch_decode(output)
    # loop over the batch to print, in this example the batch size is 1
    time_gen = time.time() - start_gen
    print(f"Load models time: {time_load_models:.2f}s")
    print(f"Generation time: {time_gen:.2f}s")
    return output

def generate_doc_ibm(project):
    url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"

    body = {
        "input": f"""Create a markdown document explaining the following project. The format of the input will be the file path of a file, followed by its content, for each file in the project. 
    Input: {project}
    Output:""",
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 200,
            "min_new_tokens": 0,
            "repetition_penalty": 1
        },
        "model_id": "ibm/granite-3-8b-instruct",
        "project_id": "c935f587-0211-4cd0-ac69-fa7f889f8a6a",
        "moderations": {
            "hap": {
                "input": {
                    "enabled": True,
                    "threshold": 0.5,
                    "mask": {
                        "remove_entity_value": True
                    }
                },
                "output": {
                    "enabled": True,
                    "threshold": 0.5,
                    "mask": {
                        "remove_entity_value": True
                    }
                }
            },
            "pii": {
                "input": {
                    "enabled": True,
                    "threshold": 0.5,
                    "mask": {
                        "remove_entity_value": True
                    }
                },
                "output": {
                    "enabled": True,
                    "threshold": 0.5,
                    "mask": {
                        "remove_entity_value": True
                    }
                }
            }
        }
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_ACCESS_TOKEN"
    }

    response = requests.post(
        url,
        headers=headers,
        json=body
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()
    return data

def main():
    start = time.time()
    project = open('tmp.txt', 'r').read()
    load_time = time.time() - start
    output = generate_doc_ibm(project)
    print(f"Load project time: {load_time:.2f}s")

if __name__ == '__main__':
    main()