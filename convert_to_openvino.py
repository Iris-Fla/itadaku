from optimum.intel.openvino import OVModelForSeq2SeqLM
from transformers import MBart50TokenizerFast

model_id = "facebook/mbart-large-50-many-to-many-mmt"

# OpenVINO用にエクスポート
model = OVModelForSeq2SeqLM.from_pretrained(model_id, export=True)
model.save_pretrained('./assets/ov_mbart')
tokenizer = MBart50TokenizerFast.from_pretrained(model_id)
tokenizer.save_pretrained('./assets/ov_mbart')