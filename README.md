# 💬 感情分析チャットボット / Sentiment Analysis Chatbot

> 日本語テキストをリアルタイムで感情分析し、ポジティブ・ネガティブ・ニュートラルをスコアリングするチャットボット。
> LINE Bot・Webアプリの2形式で動作します。

---

## 📌 目次 / Table of Contents

- [プロジェクト概要](#プロジェクト概要)
- [デモ](#デモ)
- [技術スタック](#技術スタック)
- [機能一覧](#機能一覧)
- [ファイル構成](#ファイル構成)
- [セットアップ方法](#セットアップ方法)
- [開発で直面した課題と解決策](#開発で直面した課題と解決策)
- [今後の改善予定](#今後の改善予定)

---

## プロジェクト概要

### 日本語

このプロジェクトは「日本語の感情分析チャットボット」を3つの形式で実装したものです。

- **学習の目的**：PythonのOOP・WebAPI連携・デプロイまでを一貫して学ぶ
- **感情分析の仕組み**：ポジティブ・ネガティブの単語リストによるスコアリング＋否定形への対応
- **展開形式**：コンソール版 → Webアプリ版（Streamlit）→ LINE Bot版 の順で段階的に実装

### English

A Japanese sentiment analysis chatbot that classifies user messages as Positive / Negative / Neutral with percentage scores.

Built in 3 formats: Console → Streamlit Web App → LINE Bot (deployed on Railway).

---

## デモ

### 🌐 Streamlit Web版

| チャット画面                       | サイドバー統計                     |
| ---------------------------------- | ---------------------------------- |
| _(スクリーンショットをここに追加)_ | _(スクリーンショットをここに追加)_ |

- ポジティブ・ネガティブ・ニュートラルをリアルタイムでスコア表示
- 感情に応じてUIカラーが動的に変化（緑 / 赤 / 紫）
- 会話履歴をSQLiteで永続保存（リロードしても消えない）
- 感情の推移グラフ・割合円グラフ・CSVダウンロード機能

### 📱 LINE Bot版

| 分析結果                           | 否定形対応                         |
| ---------------------------------- | ---------------------------------- |
| _(スクリーンショットをここに追加)_ | _(スクリーンショットをここに追加)_ |

- Railwayで24時間稼働中
- 「楽しくない」→ネガティブ判定など否定形に対応
- 画像・スタンプ送信時もエラーなく応答

---

## 技術スタック

| カテゴリ       | 技術                                 |
| -------------- | ------------------------------------ |
| 言語           | Python 3.14                          |
| Web UI         | Streamlit                            |
| LINE連携       | LINE Messaging API (line-bot-sdk v3) |
| Webサーバー    | Flask + Gunicorn                     |
| データベース   | SQLite3                              |
| デプロイ       | Railway                              |
| バージョン管理 | Git / GitHub                         |
| 環境変数管理   | python-dotenv                        |
| グラフ描画     | Plotly Express                       |

---

## 機能一覧

- ✅ 日本語テキストの感情スコアリング（0〜100%）
- ✅ 否定形対応（「楽しくない」→ネガティブ）
- ✅ ポジティブ・ネガティブ単語リスト（各40語以上）
- ✅ 感情に応じた返答生成
- ✅ 会話履歴のSQLite永続保存
- ✅ 感情推移の折れ線グラフ
- ✅ 感情割合の円グラフ
- ✅ 会話履歴CSVエクスポート
- ✅ 感情連動ダークテーマUI
- ✅ LINE Bot（24時間稼働・Railwayデプロイ）
- ✅ 画像・スタンプ受信時のエラーハンドリング
- ✅ 環境変数によるAPIキー管理（.env）

---

## ファイル構成

```
sentiment-bot/
├── step1_mock.py              # コンソール版（関数ベース）
├── step2_class_bot.py         # コンソール版（クラスベース）
├── step3_streamlit_chatbot.py # Streamlit Web版
├── step4_line_bot.py          # LINE Bot版（Flask）
├── requirements.txt           # 依存ライブラリ
├── Procfile                   # Railwayデプロイ設定
├── .gitignore                 # Git管理除外ファイル
└── .env                       # APIキー（Git管理外）
```

---

## セットアップ方法

### 1. リポジトリをクローン

```bash
git clone https://github.com/あなたのユーザー名/sentiment-bot.git
cd sentiment-bot
```

### 2. ライブラリをインストール

```bash
pip install -r requirements.txt
```

### 3. 環境変数を設定

`.env` ファイルを作成して以下を記入：

```
LINE_CHANNEL_SECRET=あなたのChannel Secret
LINE_CHANNEL_ACCESS_TOKEN=あなたのアクセストークン
```

### 4. 起動

**Streamlit版：**

```bash
streamlit run step3_streamlit_chatbot.py
```

**LINE Bot版（ローカル開発時）：**

```bash
python step4_line_bot.py
# 別ターミナルで
ngrok http 5000
```

---

## 開発で直面した課題と解決策

### 課題1：「楽しくない」がポジティブと誤判定される

**問題**：単語マッチングだけでは「楽しくない」の「楽し」に反応してポジティブと判定してしまう。

**原因分析**：否定形を考慮していないため、ネガティブな文脈でもポジティブ単語がヒットしてしまう。

**解決策**：単語がマッチした直後の5文字に「ない」「ず」「ません」などの否定パターンが含まれるかを追加チェックし、含まれる場合は感情スコアを反転させるロジックを実装した。

```python
after_word = message[idx + len(word):idx + len(word) + 5]
for pattern in negative_patterns:
    if pattern in after_word:
        is_negated = True
```

---

### 課題2：`.env` ファイルがフォルダとして作成されてしまう

**問題**：VS Codeで `.env` を新規作成しようとすると、ファイルではなくフォルダとして作成されてしまい、環境変数が読み込めずサーバーが起動しない。

**原因分析**：`dir .env` コマンドで確認したところ、`.env` の中に `dotenv.py` というファイルが存在しており、ファイルではなくフォルダだったことが判明。

**解決策**：VS Codeではなくメモ帳（`notepad .env`）で直接作成することで、正しくファイルとして生成できた。

---

### 課題3：LINE Bot の Webhook 検証が 502 / 404 エラーになる

**問題**：LINE DevelopersのWebhook検証を押すと毎回エラーが返ってくる。

**原因分析**：Flaskサーバーとngrokをそれぞれのターミナルで同時に起動する必要があったが、どちらかが止まっていた。またWebhookの利用がオフになっていたことも原因のひとつだった。

**解決策**：2つのターミナルで同時起動を維持することを徹底し、LINE DevelopersでWebhookの利用をオンに設定することで解決した。

---

## 今後の改善予定

| 優先度 | 内容                                             |
| ------ | ------------------------------------------------ |
| 🔴 高  | OpenAI API連携による本格的な自然言語処理への移行 |
| 🔴 高  | ユニットテストの追加（pytest）                   |
| 🟡 中  | 絵文字・カタカナ語・英語への対応                 |
| 🟡 中  | LINE Botのリッチメニュー追加                     |
| 🟡 中  | ユーザーIDごとの会話履歴管理                     |
| 🟢 低  | Streamlit版のログイン機能                        |
| 🟢 低  | デモ動画の作成・公開                             |

---

## ライセンス / License

MIT License

---

_このプロジェクトはPythonとWeb開発の学習を目的として個人で開発しました。_
