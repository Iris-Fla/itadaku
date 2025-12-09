# Itadaku - 多言語対応レストランメニュー管理システム

多言語翻訳機能を備えたレストランメニュー管理システムです。メニュー項目の名前や説明を50以上の言語に翻訳し、多様な顧客に対応できます。

## 機能

- メニュー項目の管理（追加・編集・削除）
- カテゴリによるメニューの分類
- アレルギー情報の表示
- ビーガン対応・豚肉使用有無の表示
- 多言語翻訳機能（50言語以上対応）
- 翻訳結果のキャッシュによるパフォーマンス最適化
- 商品画像のアップロードと表示

## インストール方法

### 環境

- Python 3.12
- pip（Pythonパッケージマネージャー）

### 手順

1. リポジトリをクローン

```bash
git clone https://github.com/iris-fla/itadaku.git
cd itadaku
```

2. 仮想環境を作成して有効化

```bash
# Windows
py -3.12 -m venv venv
venv\Scripts\activate

```

3. 必要なパッケージをインストール

```bash
pip install -r requirements.txt
```

4. OpenVino用翻訳モデルを作成

```bash
python convert_to_openvino.py
```

5. データベースのマイグレーション

```bash
python manage.py migrate
```

6. 管理者ユーザーの作成

```bash
python manage.py createsuperuser
```

7. 開発サーバーの起動

```bash
python manage.py runserver
```

8. ブラウザで以下のURLにアクセス
   - 管理画面: http://127.0.0.1:8000/admin/
   - メニュー一覧: http://127.0.0.1:8000/

## 使用方法

1. 管理画面にログインし、メニュー項目を追加
2. カテゴリを作成し、メニュー項目に関連付け
3. メニュー一覧ページでメニューを閲覧
4. メニュー詳細ページで多言語翻訳機能を利用

## 対応言語

facebook/mbart-large-50-one-to-many-mmtモデルを使用して、以下の言語に対応しています：

| 言語コード | 言語名 |
|------------|--------|
| ar_AR | アラビア語 |
| cs_CZ | チェコ語 |
| de_DE | ドイツ語 |
| en_XX | 英語 |
| es_XX | スペイン語 |
| fr_XX | フランス語 |
| ja_XX | 日本語 |
| ko_KR | 韓国語 |
| zh_CN | 中国語 |
| ru_RU | ロシア語 |
| ... | その他40言語以上 |

## 開発者向け情報

### プロジェクト構成

- `app/`: メインアプリケーション
  - `models.py`: データモデル定義
  - `views.py`: ビュー関数とクラス
  - `utils.py`: ユーティリティ関数
  - `templates/`: HTMLテンプレート
- `translate_ja_to_mm.py`: 翻訳機能の実装
- `itadaku/`: プロジェクト設定

### テスト用アカウント(memo)

- ユーザー名: admin
- メールアドレス: admin@test.com
- パスワード: admin