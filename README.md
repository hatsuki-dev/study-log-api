# Study Log API

FastAPIで作成した学習ログ管理APIです。  
学習内容を記録・分析し、学習状況を可視化するバックエンドアプリです。

## 機能

- 学習ログのCRUD
- タグによる検索
- 週間ログ取得
- 学習時間の統計
- タグ別ランキング
- AIによる学習アドバイス

## 使用技術

- Python
- FastAPI
- SQLAlchemy
- SQLite

## API一覧

### 学習ログ
GET /logs  
POST /logs  
GET /logs/{id}  
PUT /logs/{id}  
DELETE /logs/{id}

### 分析
GET /logs/weekly  
GET /stats  
GET /stats/tags  
GET /stats/ranking  

### AI機能
GET /ai/advice

## 今後の予定

- フロントエンド追加
- 学習時間グラフ
- AIによる学習分析の強化