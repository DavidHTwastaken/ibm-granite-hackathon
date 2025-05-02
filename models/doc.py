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

def main():
    start = time.time()
    project = open('tmp.txt', 'r').read()
    load_time = time.time() - start
    output = generate_doc(project)
    print(f"Load project time: {load_time:.2f}s")
    for i in output:
        print(i)

if __name__ == '__main__':
    main()