import streamlit as st
import random
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime


def init_db():
    conn = sqlite3.connect("chat_history.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            message TEXT,
            positive INTEGER,
            negative INTEGER,
            neutral INTEGER,
            emotion TEXT
        )"""
    )
    conn.commit()
    conn.close()


def save_message(message, scores, emotion):
    conn = sqlite3.connect("chat_history.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO messages (timestamp, message, positive, negative, neutral, emotion) VALUES (?,?,?,?,?,?)",
        (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            message,
            scores["positive"],
            scores["negative"],
            scores["neutral"],
            emotion,
        ),
    )
    conn.commit()
    conn.close()


def load_messages():
    conn = sqlite3.connect("chat_history.db")
    c = conn.cursor()
    c.execute(
        "SELECT timestamp, message, positive, negative, neutral, emotion FROM messages ORDER BY id"
    )
    rows = c.fetchall()
    conn.close()
    return rows


def clear_db():
    conn = sqlite3.connect("chat_history.db")
    c = conn.cursor()
    c.execute("DELETE FROM messages")
    conn.commit()
    conn.close()


class SentimentBot:
    def __init__(self):
        self.positive_words = [
            "楽し",
            "嬉し",
            "良",
            "幸せ",
            "最高",
            "素晴らし",
            "好き",
            "ありがとう",
            "感謝",
            "やった",
            "でき",
            "勝",
            "ハッピー",
            "ラッキー",
            "うれし",
            "たのし",
            "わくわく",
            "ドキドキ",
            "興奮",
            "癒",
            "安心",
            "希望",
            "夢",
            "成功",
            "達成",
            "褒め",
            "愛し",
            "大好き",
            "最強",
            "完璧",
            "神",
            "天才",
            "元気",
            "健康",
            "平和",
            "笑",
            "明るい",
            "充実",
        ]
        self.negative_words = [
            "悲し",
            "辛",
            "最悪",
            "嫌",
            "疲れ",
            "ダメ",
            "死ね",
            "しんど",
            "つまらな",
            "ムカつ",
            "面倒",
            "怖",
            "憂鬱",
            "落ち込",
            "絶望",
            "苦し",
            "痛",
            "泣",
            "怒",
            "イライラ",
            "不安",
            "心配",
            "悩",
            "困",
            "ストレス",
            "疲労",
            "眠れない",
            "寝れない",
            "眠れず",
            "孤独",
            "寂し",
            "虚し",
            "失敗",
            "後悔",
            "恥",
            "惨め",
            "つら",
            "きつ",
            "むかつ",
            "うざ",
            "最低",
            "終わ",
            "もう無理",
            "消えたい",
        ]
        self.responses = {
            "ポジティブ": [
                "いいね!その調子だよ!",
                "最高じゃん!",
                "それ、めっちゃいいね!",
            ],
            "ネガティブ": [
                "辛いことがあったんだね。お話聞かせてほしいな。",
                "その気持ち、めっちゃわかる。無理だけは絶対にしないでね。",
                "大変な時期だね。少しでも気持ちが楽になるといいね。",
            ],
            "ニュートラル": [
                "なるほど、そうなんですね。",
                "了解しました。",
                "そういうこともあるよ。きっと君なら乗り越えられる!",
            ],
        }
        self.score_weight = 30

    def analyze(self, message):
        negative_patterns = ["ない", "ず", "ません", "じゃない", "ではない"]
        positive_score = 0
        negative_score = 0

        for word in self.positive_words:
            if word in message:
                is_negated = False
                idx = message.find(word)
                after_word = message[idx + len(word) : idx + len(word) + 5]
                for pattern in negative_patterns:
                    if pattern in after_word:
                        is_negated = True
                        break
                if is_negated:
                    negative_score += self.score_weight
                else:
                    positive_score += self.score_weight

        for word in self.negative_words:
            if word in message:
                is_negated = False
                idx = message.find(word)
                after_word = message[idx + len(word) : idx + len(word) + 5]
                for pattern in negative_patterns:
                    if pattern in after_word:
                        is_negated = True
                        break
                if is_negated:
                    positive_score += self.score_weight
                else:
                    negative_score += self.score_weight

        neutral_score = 100 - positive_score - negative_score
        if neutral_score < 0:
            neutral_score = 0
            total = positive_score + negative_score
            positive_score = int(positive_score * 100 / total)
            negative_score = 100 - positive_score

        return {
            "positive": positive_score,
            "negative": negative_score,
            "neutral": neutral_score,
        }

    def get_emotion(self, scores):
        if scores["positive"] > scores["negative"] and scores["positive"] >= 30:
            return "ポジティブ"
        elif scores["negative"] >= 30:
            return "ネガティブ"
        else:
            dominant = max(scores, key=scores.get)
            emotion_map = {
                "positive": "ポジティブ",
                "negative": "ネガティブ",
                "neutral": "ニュートラル",
            }
            return emotion_map[dominant]

    def generate_response(self, emotion):
        return random.choice(self.responses[emotion])

    def chat(self, message):
        scores = self.analyze(message)
        emotion = self.get_emotion(scores)
        response = self.generate_response(emotion)
        return {"scores": scores, "emotion": emotion, "response": response}


init_db()

st.set_page_config(page_title="感情分析チャットボット", page_icon="💬")
st.title("💬 感情分析チャットボット")
st.caption("あなたのメッセージを感情分析します")

if "bot" not in st.session_state:
    st.session_state.bot = SentimentBot()
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("📊 統計情報")

    db_messages = load_messages()

    if db_messages:
        st.metric("総会話回数", len(db_messages))

        avg_positive = sum(r[2] for r in db_messages) / len(db_messages)
        avg_negative = sum(r[3] for r in db_messages) / len(db_messages)
        avg_neutral = sum(r[4] for r in db_messages) / len(db_messages)

        st.subheader("平均感情スコア")
        st.write(f"😊 ポジティブ: {avg_positive:.1f}%")
        st.write(f"😢 ネガティブ: {avg_negative:.1f}%")
        st.write(f"😐 ニュートラル: {avg_neutral:.1f}%")

        st.divider()

        st.subheader("📈 感情の推移")
        df = pd.DataFrame(
            db_messages,
            columns=[
                "日時",
                "メッセージ",
                "ポジティブ",
                "ネガティブ",
                "ニュートラル",
                "感情",
            ],
        )
        df["会話番号"] = range(1, len(df) + 1)
        st.line_chart(
            df.set_index("会話番号")[["ポジティブ", "ネガティブ", "ニュートラル"]]
        )

        st.divider()

        st.subheader("🎨 感情の割合")
        emotion_counts = {
            "ポジティブ": sum(1 for r in db_messages if r[5] == "ポジティブ"),
            "ネガティブ": sum(1 for r in db_messages if r[5] == "ネガティブ"),
            "ニュートラル": sum(1 for r in db_messages if r[5] == "ニュートラル"),
        }
        fig = px.pie(
            values=list(emotion_counts.values()),
            names=list(emotion_counts.keys()),
            color=list(emotion_counts.keys()),
            color_discrete_map={
                "ポジティブ": "#00D09C",
                "ネガティブ": "#FF4B4B",
                "ニュートラル": "#808495",
            },
        )
        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        csv = (
            df[
                [
                    "日時",
                    "メッセージ",
                    "ポジティブ",
                    "ネガティブ",
                    "ニュートラル",
                    "感情",
                ]
            ]
            .to_csv(index=False)
            .encode("utf-8-sig")
        )
        st.download_button(
            label="📥 会話履歴をCSVで保存",
            data=csv,
            file_name="sentiment_history.csv",
            mime="text/csv",
            use_container_width=True,
        )

    else:
        st.info("まだメッセージがありません")

    st.divider()
    if st.button("🗑️ 会話履歴をクリア", use_container_width=True):
        clear_db()
        st.session_state.messages = []
        st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "user" and "scores" in msg:
            col1, col2, col3 = st.columns(3)
            col1.metric("😊 ポジティブ", f"{msg['scores']['positive']}%")
            col2.metric("😢 ネガティブ", f"{msg['scores']['negative']}%")
            col3.metric("😐 ニュートラル", f"{msg['scores']['neutral']}%")
            st.progress(
                msg["scores"]["positive"] / 100,
                text=f"😊 ポジティブ: {msg['scores']['positive']}%",
            )
            st.progress(
                msg["scores"]["negative"] / 100,
                text=f"😢 ネガティブ: {msg['scores']['negative']}%",
            )
            st.progress(
                msg["scores"]["neutral"] / 100,
                text=f"😐 ニュートラル: {msg['scores']['neutral']}%",
            )
            if "emotion" in msg:
                st.info(f"🎯 主な感情: {msg['emotion']}")

user_input = st.chat_input("メッセージを入力...")

if user_input:
    result = st.session_state.bot.chat(user_input)
    save_message(user_input, result["scores"], result["emotion"])

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
            "scores": result["scores"],
            "emotion": result["emotion"],
        }
    )
    st.session_state.messages.append(
        {"role": "assistant", "content": result["response"]}
    )
    st.rerun()
