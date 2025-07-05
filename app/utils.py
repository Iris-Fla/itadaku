import os
from typing import Dict, Optional, Tuple, List, Any
from django.conf import settings
from .models import TranslationCache

# translate_ja_to_mm.pyからの関数をインポート
from translate_ja_to_mm import (
    translate_text as translate_text_base,
    get_supported_languages,
    get_language_name
)


def get_translation_cache(content_type: str, object_id: int, field_name: str, target_language: str) -> Optional[str]:
    """
    翻訳キャッシュを取得する関数
    
    Args:
        content_type: コンテンツタイプ（例: 'menu_item'）
        object_id: オブジェクトID
        field_name: フィールド名（例: 'name', 'description'）
        target_language: 翻訳先言語コード（例: 'en_XX'）
        
    Returns:
        キャッシュがある場合は翻訳されたテキスト、ない場合はNone
    """
    try:
        cache = TranslationCache.objects.get(
            content_type=content_type,
            object_id=object_id,
            field_name=field_name,
            target_language=target_language
        )
        return cache.translated_text
    except TranslationCache.DoesNotExist:
        return None


def save_translation_cache(content_type: str, object_id: int, field_name: str, 
                          source_text: str, target_language: str, translated_text: str) -> None:
    """
    翻訳結果をキャッシュに保存する関数
    
    Args:
        content_type: コンテンツタイプ（例: 'menu_item'）
        object_id: オブジェクトID
        field_name: フィールド名（例: 'name', 'description'）
        source_text: 元のテキスト
        target_language: 翻訳先言語コード（例: 'en_XX'）
        translated_text: 翻訳されたテキスト
    """
    # 既存のキャッシュがあれば更新、なければ作成
    TranslationCache.objects.update_or_create(
        content_type=content_type,
        object_id=object_id,
        field_name=field_name,
        target_language=target_language,
        defaults={
            'source_text': source_text,
            'translated_text': translated_text
        }
    )


def translate_text_with_cache(text: str, content_type: str, object_id: int, 
                             field_name: str, target_language: str = 'en_XX') -> str:
    """
    キャッシュを利用して翻訳を行う関数
    
    Args:
        text: 翻訳するテキスト
        content_type: コンテンツタイプ
        object_id: オブジェクトID
        field_name: フィールド名
        target_language: 翻訳先言語コード（デフォルト: 'en_XX'）
        
    Returns:
        翻訳されたテキスト
    """
    # 空のテキストは翻訳しない
    if not text:
        return ""
        
    # キャッシュを確認
    cached_translation = get_translation_cache(
        content_type, object_id, field_name, target_language
    )
    
    # キャッシュがあればそれを返す
    if cached_translation is not None:
        return cached_translation
    
    # キャッシュがなければ翻訳して保存
    try:
        translated_text = translate_text_base(text, target_language)
        save_translation_cache(
            content_type, object_id, field_name, text, target_language, translated_text
        )
        return translated_text
    except Exception as e:
        # 翻訳に失敗した場合はエラーをログに記録し、元のテキストを返す
        print(f"翻訳エラー: {e}")
        return text


def get_available_languages() -> List[Tuple[str, str]]:
    """
    利用可能な言語のリストを取得する関数
    
    Returns:
        言語コードと言語名のタプルのリスト
    """
    languages = get_supported_languages()
    return [(code, name) for code, name in languages.items()]