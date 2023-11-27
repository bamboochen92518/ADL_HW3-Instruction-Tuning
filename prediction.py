import torch
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer
import json
from peft import PeftModel
from utils import get_prompt, get_bnb_config
import argparse

pred_file = 'prediction.json'

def predict(model, tokenizer, data, max_length=2048,):
    data_size = len(data)
    instructions = [get_prompt(x["instruction"]) for x in data]

    # Tokenize data
    tokenized_instructions = tokenizer(instructions, add_special_tokens=False)

    # Format data
    for i in range(data_size):
        tokenized_instructions["attention_mask"][i] = [
            1] * len(tokenized_instructions["input_ids"][i])

        tokenized_instructions["input_ids"][i] = torch.tensor(
            tokenized_instructions["input_ids"][i][:max_length])
        tokenized_instructions["attention_mask"][i] = torch.tensor(
            tokenized_instructions["attention_mask"][i][:max_length])

    # Calculate ppl
    outs = []
    for i in tqdm(range(data_size)):
        input_ids = tokenized_instructions["input_ids"][i].unsqueeze(0)
        attn_mask = tokenized_instructions["attention_mask"][i].unsqueeze(0)

        with torch.no_grad():
            generate = model.generate(input_ids=input_ids, attention_mask=attn_mask)
            pred = tokenizer.batch_decode(generate.detach().cpu().numpy(), skip_special_tokens=True)
            pred = pred[0].split('>>')[-1]
            outs.append(pred)
            print(pred)

    index = 0
    for d in data:
        d['output'] = outs[index]
        del d['instruction']
        index += 1
    with open(pred_file, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base_model_path",
        type=str,
        default="Taiwan-LLM-7B-v2.0-chat",
        help="Path to the checkpoint of Taiwan-LLM-7B-v2.0-chat. If not set, this script will use "
        "the checkpoint from Huggingface (revision = 5073b2bbc1aa5519acdc865e99832857ef47f7c9)."
    )
    parser.add_argument(
        "--peft_path",
        type=str,
        required=True,
        help="Path to the saved PEFT checkpoint."
    )
    parser.add_argument(
        "--test_data_path",
        type=str,
        default="data/new_public_test.json",
        help="Path to test data."
    )
    args = parser.parse_args()

    # Load model
    bnb_config = get_bnb_config()

    model = AutoModelForCausalLM.from_pretrained(
        args.base_model_path,
        torch_dtype=torch.bfloat16,
        quantization_config=bnb_config
    )
    tokenizer = AutoTokenizer.from_pretrained(args.base_model_path)

    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id

    # Load LoRA
    model = PeftModel.from_pretrained(model, args.peft_path)

    with open(args.test_data_path, "r") as f:
        data = json.load(f)

    model.eval()
    predict(model, tokenizer, data)
