from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import MenuItem, MenuCategory, TranslationCache
from .utils import translate_text_with_cache, get_available_languages

class MenuListView(ListView):
    model = MenuItem
    template_name = 'app/menu_list.html'
    context_object_name = 'menu_items'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = MenuCategory.objects.all().order_by('display_order')
        
        # 利用可能な言語のリストに国コードを追加
        available_languages = get_available_languages()
        languages_with_flags = []
        for code, name in available_languages:
            country_code = code.split('_')[-1].lower()
            if country_code == 'xx': # 'en_XX'のような場合
                country_code = 'us' if code == 'en_XX' else 'un' # enはus、その他は国連旗
            elif country_code == 'cn':
                country_code = 'cn'
            elif code == 'ja_XX':
                country_code = 'jp'
            languages_with_flags.append((code, name, country_code))
        
        context['available_languages'] = languages_with_flags
        context['selected_language'] = self.request.GET.get('lang', 'ja_XX')
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # カテゴリでフィルタリング
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(categories__category_id=category_id)
        
        # アレルギーでフィルタリング
        allergen_filter = self.request.GET.getlist('allergen')
        if allergen_filter:
            for allergen in allergen_filter:
                # JSONFieldから特定のアレルギー物質を含まないものをフィルタリング
                queryset = queryset.exclude(allergens__contains=[allergen])
        
        # ビーガン対応でフィルタリング
        vegan_filter = self.request.GET.get('vegan')
        if vegan_filter == 'true':
            queryset = queryset.filter(is_vegan=True)
        
        # 豚肉でフィルタリング
        pork_filter = self.request.GET.get('pork')
        if pork_filter == 'false':
            queryset = queryset.filter(contains_pork=False)
        
        return queryset

class MenuItemDetailView(DetailView):
    model = MenuItem
    template_name = 'app/menu_item_detail.html'
    context_object_name = 'menu_item'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 利用可能な言語のリストを追加
        context['available_languages'] = get_available_languages()
        # 選択された言語（デフォルトは日本語）
        context['selected_language'] = self.request.GET.get('lang', 'ja_XX')
        return context

@require_http_methods(["GET"])
def translate_menu_item(request, pk):
    """メニュー項目の翻訳APIエンドポイント"""
    # デバッグ情報を出力
    print(f"翻訳APIが呼び出されました: pk={pk}, GET={request.GET}")
    
    # パラメータの取得
    field_name = request.GET.get('field', '')
    target_language = request.GET.get('lang', 'en_XX')
    
    # パラメータのバリデーション
    if not field_name or not target_language:
        print(f"バリデーションエラー: field_name={field_name}, target_language={target_language}")
        return JsonResponse({'error': '必須パラメータが不足しています'}, status=400)
    
    # メニュー項目の取得
    try:
        menu_item = get_object_or_404(MenuItem, pk=pk)
        print(f"メニュー項目を取得しました: id={menu_item.id}, name={menu_item.name}")
    except Exception as e:
        print(f"メニュー項目の取得に失敗しました: pk={pk}, error={e}")
        return JsonResponse({'error': 'メニュー項目が見つかりません'}, status=404)
    
    # 翻訳対象のフィールドの値を取得
    if field_name == 'name':
        text = menu_item.name
    elif field_name == 'description':
        text = menu_item.description
    else:
        print(f"無効なフィールド名: {field_name}")
        return JsonResponse({'error': '無効なフィールド名です'}, status=400)
    
    print(f"翻訳を実行します: text={text}, target_language={target_language}")
    
    # 翻訳の実行（キャッシュを利用）
    try:
        translated_text = translate_text_with_cache(
            text, 'menu_item', menu_item.id, field_name, target_language
        )
        print(f"翻訳結果: {translated_text}")
    except Exception as e:
        print(f"翻訳エラー: {e}")
        return JsonResponse({'error': f'翻訳処理中にエラーが発生しました: {str(e)}'}, status=500)
    
    # 結果を返す
    response_data = {
        'original': text,
        'translated': translated_text,
        'language': target_language
    }
    print(f"レスポンス: {response_data}")
    return JsonResponse(response_data)
