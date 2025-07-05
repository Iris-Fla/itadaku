from optimum.intel.openvino import OVModelForSeq2SeqLM
from transformers import MBart50TokenizerFast
import os
from typing import Dict, Optional, Tuple

# 対応言語コードと言語名のマッピング
SUPPORTED_LANGUAGES: Dict[str, str] = {
    "ar_AR": "アラビア語",
    "cs_CZ": "チェコ語",
    "de_DE": "ドイツ語",
    "en_XX": "英語",
    "es_XX": "スペイン語",
    "et_EE": "エストニア語",
    "fi_FI": "フィンランド語",
    "fr_XX": "フランス語",
    "gu_IN": "グジャラート語",
    "hi_IN": "ヒンディー語",
    "it_IT": "イタリア語",
    "ja_XX": "日本語",
    "kk_KZ": "カザフ語",
    "ko_KR": "韓国語",
    "lt_LT": "リトアニア語",
    "lv_LV": "ラトビア語",
    "my_MM": "ビルマ語",
    "ne_NP": "ネパール語",
    "nl_XX": "オランダ語",
    "ro_RO": "ルーマニア語",
    "ru_RU": "ロシア語",
    "si_LK": "シンハラ語",
    "tr_TR": "トルコ語",
    "vi_VN": "ベトナム語",
    "zh_CN": "中国語",
    "af_ZA": "アフリカーンス語",
    "az_AZ": "アゼルバイジャン語",
    "bn_IN": "ベンガル語",
    "fa_IR": "ペルシア語",
    "he_IL": "ヘブライ語",
    "hr_HR": "クロアチア語",
    "id_ID": "インドネシア語",
    "ka_GE": "グルジア語",
    "km_KH": "クメール語",
    "mk_MK": "マケドニア語",
    "ml_IN": "マラヤーラム語",
    "mn_MN": "モンゴル語",
    "mr_IN": "マラーティー語",
    "pl_PL": "ポーランド語",
    "ps_AF": "パシュトゥー語",
    "pt_XX": "ポルトガル語",
    "sv_SE": "スウェーデン語",
    "sw_KE": "スワヒリ語",
    "ta_IN": "タミル語",
    "te_IN": "テルグ語",
    "th_TH": "タイ語",
    "tl_XX": "タガログ語",
    "uk_UA": "ウクライナ語",
    "ur_PK": "ウルドゥー語",
    "xh_ZA": "コサ語",
    "gl_ES": "ガリシア語",
    "sl_SI": "スロベニア語",
}

# モデルとトークナイザーのキャッシュ
_model = None
_tokenizer = None


def get_model_and_tokenizer() -> Tuple[OVModelForSeq2SeqLM, MBart50TokenizerFast]:
    """
    モデルとトークナイザーをロードし、キャッシュする関数

    Returns:
        Tuple[OVModelForSeq2SeqLM, MBart50TokenizerFast]: モデルとトークナイザーのタプル
    """
    global _model, _tokenizer

    if _model is None or _tokenizer is None:
        model_dir = "./assets/ov_mbart"

        if not os.path.exists(model_dir):
            raise FileNotFoundError(f"モデルディレクトリが見つかりません: {model_dir}")

        _model = OVModelForSeq2SeqLM.from_pretrained(model_dir)
        _tokenizer = MBart50TokenizerFast.from_pretrained(model_dir)

    return _model, _tokenizer


def get_supported_languages() -> Dict[str, str]:
    """
    サポートされている言語コードと言語名のマッピングを取得する関数

    Returns:
        Dict[str, str]: 言語コードと言語名のマッピング
    """
    return SUPPORTED_LANGUAGES.copy()


def translate_text(japanese_text: str, target_lang: str = "en_XX") -> str:
    """
    日本語テキストを指定された言語に翻訳する関数

    Args:
        japanese_text (str): 翻訳したい日本語テキスト
        target_lang (str): 翻訳先の言語コード（デフォルト: en_XX）
                          例: en_XX（英語）, zh_CN（中国語）, ko_KR（韓国語）など

    Returns:
        str: 翻訳されたテキスト

    Raises:
        ValueError: サポートされていない言語コードが指定された場合
    """
    # 言語コードの検証
    if target_lang not in SUPPORTED_LANGUAGES:
        supported_codes = ", ".join(SUPPORTED_LANGUAGES.keys())
        raise ValueError(
            f"サポートされていない言語コードです: {target_lang}\nサポートされている言語コード: {supported_codes}"
        )

    # モデルとトークナイザーの取得
    model, tokenizer = get_model_and_tokenizer()

    # 入力テキストの準備
    tokenizer.src_lang = "ja_XX"  # 入力は日本語
    inputs = tokenizer(japanese_text, return_tensors="pt")

    # 翻訳の実行
    generated_tokens = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        forced_bos_token_id=tokenizer.lang_code_to_id[target_lang],
        max_new_tokens=50,
    )

    # 翻訳結果のデコード
    translated_text = tokenizer.batch_decode(
        generated_tokens, skip_special_tokens=True
    )[0]

    return translated_text


def get_language_name(lang_code: str) -> Optional[str]:
    """
    言語コードから言語名を取得する関数

    Args:
        lang_code (str): 言語コード

    Returns:
        Optional[str]: 言語名（サポートされていない言語コードの場合はNone）
    """
    return SUPPORTED_LANGUAGES.get(lang_code)


# 使用例
if __name__ == "__main__":
    # 英語への翻訳例
    ja_text = "えび、かに、たまご"
    en_translation = translate_text(ja_text, "en_XX")
    print(f"日本語: {ja_text}")
    print(f"英語訳: {en_translation}")

    # 中国語への翻訳例
    zh_translation = translate_text(ja_text, "zh_CN")
    print(f"中国語訳: {zh_translation}")

    # 韓国語への翻訳例
    ko_translation = translate_text(ja_text, "ko_KR")
    print(f"韓国語訳: {ko_translation}")

    # サポートされている言語の一覧表示
    print("\n対応言語一覧:")
    for code, name in sorted(get_supported_languages().items()):
        print(f"  {code}: {name}")

    # 使用例: 言語名の取得
    lang_code = "fr_XX"
    lang_name = get_language_name(lang_code)
    print(f"\n言語コード '{lang_code}' の言語名: {lang_name}")
