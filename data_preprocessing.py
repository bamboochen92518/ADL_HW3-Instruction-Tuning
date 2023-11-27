import json
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--in_file", type=str, default="train.json")
parser.add_argument("--out_file", type=str, default="train.jsonl")
args = parser.parse_args()

file_name = [args.in_file]

q1_list = ['翻譯成文言文：', '幫我把這句話翻譯成文言文', '這句話在古代怎麼說：', '把這句話翻譯成文言文：', '將下麵句子翻譯成文言文：', '這句話在中國古代怎麼說：', '翻譯成古文：']

q2_list = ['文言文翻譯：', '把這句話翻譯成現代文。', '翻譯成現代文：', '將下麵句子翻譯成現代文：', '翻譯成白話文：', '幫我把這句話翻譯成現代文']

for file in file_name:
    with open(file, "r") as f:
        data = json.load(f)
    for d in data:
        tmp = d["instruction"].split('\n')
        success = 0
        for i in range(2):
            if tmp[i] in q1_list:
                success = i
                tmp[i] = "把這句話翻譯成文言文："
            if tmp[i] in q2_list:
                success = i
                tmp[i] = "把這句話翻譯成白話文："
        if success == 0:
            d["instruction"] = tmp[0] + tmp[1]
        else:
            d["instruction"] = tmp[1] + tmp[0]


    with open(args.out_file, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

