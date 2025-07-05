from optimum.intel.openvino import OVModelForSeq2SeqLM
from transformers import MBart50TokenizerFast

model_dir = "./assets/ov_mbart"

model = OVModelForSeq2SeqLM.from_pretrained(model_dir)
tokenizer = MBart50TokenizerFast.from_pretrained(model_dir)

text_ja = "えび、かに、たまご"

tokenizer.src_lang = "ja_XX"
inputs = tokenizer(text_ja, return_tensors="pt")

generated_tokens = model.generate(
    input_ids=inputs["input_ids"],
    attention_mask=inputs["attention_mask"],  # 追加
    forced_bos_token_id=tokenizer.lang_code_to_id["en_XX"],
    max_new_tokens=50
)

translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
print(translated_text)