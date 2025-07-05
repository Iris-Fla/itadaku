from django.core.management.base import BaseCommand
from app.models import MenuItem, MenuCategory, MenuItemCategory

class Command(BaseCommand):
    help = 'レストランメニューのサンプルデータを作成します'

    def handle(self, *args, **options):
        # カテゴリの作成
        categories = {
            'main': MenuCategory.objects.create(name='メイン料理', display_order=1),
            'side': MenuCategory.objects.create(name='サイドメニュー', display_order=2),
            'dessert': MenuCategory.objects.create(name='デザート', display_order=3),
            'drink': MenuCategory.objects.create(name='ドリンク', display_order=4),
        }
        
        # メニュー項目の作成
        menu_items = [
            # メイン料理
            {
                'name': '牛ステーキ',
                'price': 2800,
                'description': '厳選された牛肉を使用した贅沢なステーキです。',
                'allergens': ['milk'],
                'is_vegan': False,
                'contains_pork': False,
                'categories': ['main'],
            },
            {
                'name': '豚の生姜焼き',
                'price': 1200,
                'description': '国産豚肉を使用した定番の生姜焼きです。',
                'allergens': ['wheat', 'soy'],
                'is_vegan': False,
                'contains_pork': True,
                'categories': ['main'],
            },
            {
                'name': 'ベジタブルカレー',
                'price': 1000,
                'description': '季節の野菜をたっぷり使ったカレーです。',
                'allergens': ['wheat'],
                'is_vegan': True,
                'contains_pork': False,
                'categories': ['main'],
            },
            # サイドメニュー
            {
                'name': 'フライドポテト',
                'price': 500,
                'description': 'カリッと揚げたポテトフライです。',
                'allergens': [],
                'is_vegan': True,
                'contains_pork': False,
                'categories': ['side'],
            },
            {
                'name': 'シーザーサラダ',
                'price': 700,
                'description': '新鮮な野菜とシーザードレッシングのサラダです。',
                'allergens': ['egg', 'milk', 'wheat'],
                'is_vegan': False,
                'contains_pork': False,
                'categories': ['side'],
            },
            # デザート
            {
                'name': 'チョコレートケーキ',
                'price': 600,
                'description': '濃厚なチョコレートケーキです。',
                'allergens': ['egg', 'milk', 'wheat'],
                'is_vegan': False,
                'contains_pork': False,
                'categories': ['dessert'],
            },
            {
                'name': 'フルーツパフェ',
                'price': 800,
                'description': '季節のフルーツを使ったパフェです。',
                'allergens': ['milk', 'fruit'],
                'is_vegan': False,
                'contains_pork': False,
                'categories': ['dessert'],
            },
            # ドリンク
            {
                'name': 'コーヒー',
                'price': 400,
                'description': '香り高いコーヒーです。',
                'allergens': [],
                'is_vegan': True,
                'contains_pork': False,
                'categories': ['drink'],
            },
            {
                'name': 'オレンジジュース',
                'price': 450,
                'description': '搾りたてのオレンジジュースです。',
                'allergens': ['fruit'],
                'is_vegan': True,
                'contains_pork': False,
                'categories': ['drink'],
            },
        ]
        
        # メニュー項目の登録
        for item_data in menu_items:
            # カテゴリを一時的に取り出す
            categories_data = item_data.pop('categories')
            
            # メニュー項目を作成
            menu_item = MenuItem.objects.create(**item_data)
            
            # カテゴリとの関連付けを作成
            for category_key in categories_data:
                MenuItemCategory.objects.create(
                    menu_item=menu_item,
                    category=categories[category_key]
                )
        
        self.stdout.write(self.style.SUCCESS(f'{len(menu_items)}件のメニュー項目を作成しました'))