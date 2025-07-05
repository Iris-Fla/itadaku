from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

# アレルギー物質の選択肢
ALLERGEN_CHOICES = [
    ('egg', '卵'),
    ('milk', '乳'),
    ('wheat', '小麦'),
    ('shrimp', 'えび'),
    ('crab', 'かに'),
    ('peanut', '落花生'),
    ('soba', 'そば'),
    ('fish', '魚'),
    ('nuts', 'ナッツ類'),
    ('soy', '大豆'),
    ('fruit', '果物'),
    ('sesame', 'ごま'),
]

class MenuItem(models.Model):
    """レストランメニュー項目モデル"""
    name = models.CharField('商品名', max_length=100)
    price = models.PositiveIntegerField('価格', validators=[MinValueValidator(0)])
    description = models.TextField('商品詳細', blank=True)
    
    # タイトル画像
    image = models.ImageField('商品画像', upload_to='menu_images/', blank=True, null=True)
    
    # アレルギー情報（複数選択可能）
    allergens = models.JSONField('アレルギー物質', default=list, blank=True, help_text='含まれるアレルギー物質')
    
    # 食事制限関連
    is_vegan = models.BooleanField('ビーガン対応', default=False)
    contains_pork = models.BooleanField('豚肉含有', default=False)
    
    # 管理用フィールド
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)
    is_available = models.BooleanField('提供可能', default=True)
    
    class Meta:
        verbose_name = 'メニュー項目'
        verbose_name_plural = 'メニュー項目'
        ordering = ['name']
    
    def __str__(self):
        return f'{self.name} (¥{self.price})'
    
    def get_allergens_display(self):
        """アレルギー物質の表示名を取得"""
        allergen_dict = dict(ALLERGEN_CHOICES)
        return [allergen_dict.get(a, a) for a in self.allergens]
    
    def has_allergen(self, allergen_code):
        """特定のアレルギー物質が含まれているかチェック"""
        return allergen_code in self.allergens


class MenuCategory(models.Model):
    """メニューカテゴリモデル"""
    name = models.CharField('カテゴリ名', max_length=50)
    description = models.TextField('説明', blank=True)
    display_order = models.PositiveIntegerField('表示順', default=0)
    
    class Meta:
        verbose_name = 'メニューカテゴリ'
        verbose_name_plural = 'メニューカテゴリ'
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return self.name


class MenuItemCategory(models.Model):
    """メニュー項目とカテゴリの関連付けモデル"""
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='categories')
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='menu_items')
    
    class Meta:
        verbose_name = 'メニュー項目カテゴリ'
        verbose_name_plural = 'メニュー項目カテゴリ'
        unique_together = ('menu_item', 'category')
    
    def __str__(self):
        return f'{self.menu_item.name} - {self.category.name}'


class TranslationCache(models.Model):
    """翻訳結果のキャッシュモデル"""
    # 翻訳元のコンテンツタイプ（メニュー名、説明など）
    content_type = models.CharField('コンテンツタイプ', max_length=50)
    # 翻訳元のオブジェクトID
    object_id = models.PositiveIntegerField('オブジェクトID')
    # 翻訳元のフィールド名
    field_name = models.CharField('フィールド名', max_length=50)
    # 翻訳元のテキスト
    source_text = models.TextField('元のテキスト')
    # 翻訳先の言語コード
    target_language = models.CharField('翻訳先言語', max_length=10)
    # 翻訳されたテキスト
    translated_text = models.TextField('翻訳されたテキスト')
    # キャッシュの作成日時
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    # 最終更新日時
    updated_at = models.DateTimeField('更新日時', auto_now=True)
    
    class Meta:
        verbose_name = '翻訳キャッシュ'
        verbose_name_plural = '翻訳キャッシュ'
        # 同じコンテンツの同じフィールドの同じ言語への翻訳は一意
        unique_together = ('content_type', 'object_id', 'field_name', 'target_language')
        # キャッシュヒット率を上げるためのインデックス
        indexes = [
            models.Index(fields=['content_type', 'object_id', 'field_name', 'target_language']),
        ]
    
    def __str__(self):
        return f'{self.content_type}:{self.object_id}:{self.field_name} -> {self.target_language}'
