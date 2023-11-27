from transformers import BitsAndBytesConfig
import torch


def get_prompt(instruction: str) -> str:
    '''Format the instruction as a prompt for LLM.'''
    return f"把這句話翻譯成白話文：秦王惡之，後戒左右贊來不得通，贊亦不往，月一至府而已，退則杜門不交人事。 >> 秦王討厭他，後來告誡手下人劉贊來瞭不得通報，劉贊也不去，每月去王府一次罷瞭，迴來後就閉門不齣，不和人交往。把這句話翻譯成文言文：老虎發怒，直嚮皇上撲來，左右均退避，昭袞棄馬，翻身躍上虎背揪住虎的雙耳，老虎大驚，想要逃走。>> 虎怒，奮勢將犯蹕。左右闢易，昭袞捨馬，捉虎兩耳騎之。{instruction} >>"
def get_bnb_config() -> BitsAndBytesConfig:
    '''Get the BitsAndBytesConfig.'''
    quantization_config=BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type='nf4',
        )
    return quantization_config
