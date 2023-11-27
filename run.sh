#!/bin/bash
python data_preprocessing.py --in_file ${3} --out_file tmp.json
python prediction.py --base_model_path ${1} --peft_path ${2} --test_data_path tmp.json --output_path ${4}
