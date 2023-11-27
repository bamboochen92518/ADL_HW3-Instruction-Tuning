# ADL HW3 Instruction-Tuning

## 執行

```bash
bash ./download.sh
bash ./run.sh /path/to/Taiwan-LLaMa-folder /path/to/adapter_checkpoint \ /path/to/input.json /path/to/output.json
```

### `download.sh`

下載訓練完成的模型。

### `run.sh`

將測試資料輸入模型，並輸出預測結果。

## 完整訓練過程

#### Step 1 統一問題格式

```bash
$ python data_preprocessing.py --in_file ${3} --out_file tmp.json
$ python data_preprocessing.py --in_file train.json --out_file new_train.json
```

這步完成之後會分別將問題的格式統一。所有白話文翻成文言文的問題都會統一為「把這句話翻譯成文言文」，所有文言文翻成白話文的問題都會統一為「把這句話翻譯成白話文」。

#### Step 2 把 train data 加上 prompt

```bash
$ python train_addprompt.py
```

這步完成之後會將`new_train.json`轉成`new_train_with_prompt.json`。

#### Step 3 Training

```bash
$ python -m axolotl.cli.train qlora.yml
```

所有使用到的參數在`qlora.yml`裡面，其餘請參考https://github.com/OpenAccess-AI-Collective/axolotl/tree/main。

這步完成之後會產生`adapter_checkpoint `。

#### Step 4 Prediction

```bash
$ python prediction.py --base_model_path ${1} --peft_path ${2} --test_data_path tmp.json --output_path ${4}
```

這步完成之後會產生最終的預測結果。
