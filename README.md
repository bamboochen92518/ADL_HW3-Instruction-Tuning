# Applied Deep Learning HW3 <br>Instruction-Tuning

### Task Description

In this task, there are two subtasks: one involves translating Classical Chinese (文言文) into Vernacular Chinese (白話文), and the other involves translating Vernacular Chinese into Classical Chinese. Our objective is to identify the most effective prompt for generating the response.

### 執行

```bash
bash ./download.sh
bash ./run.sh /path/to/Taiwan-LLaMa-folder /path/to/adapter_checkpoint \ /path/to/input.json /path/to/output.json
```

#### `download.sh`

Download the trained model.

#### `run.sh`

Input the test data into the model and generate the predicted results.

### Complete Training Process

##### Step 1 Standardize the question format

```bash
$ python data_preprocessing.py --in_file ${3} --out_file tmp.json
$ python data_preprocessing.py --in_file train.json --out_file new_train.json
```

After completing this step, the formats of the questions will be standardized separately. All questions related to translating Vernacular Chinese into Classical Chinese will be unified as '把這句話翻譯成文言文,' and all questions related to translating Classical Chinese into Vernacular Chinese will be standardized as '把這句話翻譯成白話文.'

##### Step 2 Add prompts to the training data

```bash
$ python train_addprompt.py
```

After completing this step, `new_train.json` will be transformed into `new_train_with_prompt.json`.

##### Step 3 Training

```bash
$ python -m axolotl.cli.train qlora.yml
```

All the parameters used are in `qlora.yml`; for the rest, please refer to https://github.com/OpenAccess-AI-Collective/axolotl/tree/main.

Upon completion of this step, `adapter_checkpoint` will be generated.

##### Step 4 Prediction

```bash
$ python prediction.py --base_model_path ${1} --peft_path ${2} --test_data_path tmp.json --output_path ${4}
```

After completing this step, the final prediction results will be generated.

Homework Spec: 

https://docs.google.com/presentation/d/1bZyF83pI9WZq558QDNsO9E7vl2B6PQJLLpu4V5EBo9A/edit#slide=id.g2976d025caf_0_126
