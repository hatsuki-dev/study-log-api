# Study Log API

FastAPIで作成した学習ログ管理APIです。  
学習内容を記録・分析し、学習状況を可視化するバックエンドアプリです。

## アプリ画面

![Study Dashboard](images/dashboard.png)

---

# 機能

- 学習ログのCRUD
- タグによる検索
- 週間ログ取得
- 学習時間の統計
- タグ別ランキング
- AIによる学習アドバイス

---

# 使用技術

## Backend

- Python
- FastAPI
- SQLAlchemy
- SQLite

## Frontend

- React
- Chart.js
- JavaScript

---

# API一覧

## 学習ログ

GET /logs  
POST /logs  
GET /logs/{id}  
PUT /logs/{id}  
DELETE /logs/{id}

## 分析

GET /logs/weekly  
GET /stats  
GET /stats/tags  
GET /stats/ranking  

## AI機能

GET /ai/advice

---

# フロントエンド

このAPIを利用した学習ダッシュボードをReactで作成しています。

主な機能

- 学習ログ追加
- 学習ログ編集
- 学習ログ削除
- 学習時間グラフ表示
- 総学習時間表示

---

# アプリ構成

React (Frontend)  
↓  
FastAPI (Backend API)  
↓  
SQLite (Database)

---

# 起動方法

## Backend

```bash
uvicorn main:app --reload
```

## Frontend

```bash
npm run dev
```

Frontend URL

```
http://localhost:5173
```

Backend URL

```
http://127.0.0.1:8000
```

---

# 今後の拡張

- 学習継続日数（streak）
- 週間学習時間グラフ
- タグ別学習分析
- AIによる学習レポート