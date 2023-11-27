# ADL HW2 Chinese News Summarization

## 執行

```bash
bash ./download.sh
bash ./run.sh /path/to/input.jsonl /path/to/output.jsonl
```

### `download.sh`

下載訓練完成的模型。

### `run.sh`

將測試資料輸入模型，並輸出預測結果。

## 完整訓練過程

#### Step 1 Turn jsonl file to json file

```bash
$ python jsonl_to_json.py --in_file ${1} --out_file tmp.json --test
$ python3 jsonl_to_json.py --in_file train.jsonl --out_file train.json
```

這步完成之後會分別將`input.jsonl`和`train.jsonl`轉換成`tmp.json`和`train.json`，因為 input file 沒有 title 那一欄，所以要特別加一個參數區分。

#### Step 2 Training

```bash
$ python train.py
```

這步完成之後會產生訓練完的 model。

程式碼主要是從 `run_summarization_no_trainer.py`[1] 做修改，只取訓練的部份，將 validation 的過程刪除。

使用的 hyper parameter 如下：

| arguments                       | value               |
| ------------------------------- | ------------------- |
| `--train_file`                  | `./data/train.json` |
| `--max_source_length`           | `1024`              |
| `--max_target_length`           | `64`                |
| `--model_name_or_path`          | `google/mt5-small`  |
| `--text_column`                 | `maintext`          |
| `--summary_column`              | `title`             |
| `--per_device_train_batch_size` | `4`                 |
| `--learning_rate`               | `1e-4`              |
| `--num_train_epochs`            | `10`                |
| `--gradient_accumulation_steps` | `4`                 |
| `--output_dir`                  | `model_e10b4`       |
| `--seed`                        | `42`                |

#### Step 3 Testing

```bash
$ python test.py
```

程式碼主要是從 `run_summarization_no_trainer.py`[1] 做修改，只取 validation 的部份，並輸出最後的預測結果，以`json`格式輸出。

此外，還有新增以下的超參數：

1. 加入 sampling 參數，例如：`top_k`, `top_p`, `do_sampling`。
2. 加入 generation controlling 參數，例如：`temperature`, `length_penalty`, `repetition`。

使用的 hyper parameter 如下：

| arguments                 | value             |
| ------------------------- | ----------------- |
| `--validation_file`       | `./data/tmp.json` |
| `--output_file`           | `prediction.json` |
| `--max_source_length`     | `1024`            |
| `--val_max_target_length` | `64`              |
| `--num_beams`             | `5`               |
| `--temperature`           | `0.5`             |
| `--model_name_or_path`    | `model_e10b4`     |
| `--text_column`           | `maintext`        |
| `--summary_column`        | `title`           |

在 report 中會解釋為什麼選擇 beam search 而非 top k or top p sampling。

#### Step 4 turn json file to jsonl file

```bash
$ python json_to_jsonl.py --in_file prediction.json --out_file ${2}
```

由於最後要輸出`jsonl`格式，所以要再把`json`轉成`jsonl`。

相關資料：

[1] `run_summarization_no_trainer.py`原始碼

https://github.com/huggingface/transformers/blob/main/examples/pytorch/summarization/run_summarization_no_trainer.py

[2] Summarization 相關資料

https://huggingface.co/docs/transformers/tasks/summarization
