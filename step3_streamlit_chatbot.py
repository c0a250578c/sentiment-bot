import streamlit as st
import random
import pandas as pd
import plotly.express as px


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


st.set_page_config(page_title="感情分析チャットボット", page_icon="💬")
st.title("💬 感情分析チャットボット")
st.caption("あなたのメッセージを感情分析します")

if "bot" not in st.session_state:
    st.session_state.bot = SentimentBot()
    st.session_state.messages = []

with st.sidebar:
    st.header("📊 統計情報")

    if st.session_state.messages:
        total_messages = len(
            [m for m in st.session_state.messages if m["role"] == "user"]
        )
        st.metric("会話回数", total_messages)

        user_messages = [
            m
            for m in st.session_state.messages
            if m["role"] == "user" and "scores" in m
        ]

        if user_messages:
            avg_positive = sum(m["scores"]["positive"] for m in user_messages) / len(
                user_messages
            )
            avg_negative = sum(m["scores"]["negative"] for m in user_messages) / len(
                user_messages
            )
            avg_neutral = sum(m["scores"]["neutral"] for m in user_messages) / len(
                user_messages
            )

            st.subheader("平均感情スコア")
            st.write(f"😊 ポジティブ: {avg_positive:.1f}%")
            st.write(f"😢 ネガティブ: {avg_negative:.1f}%")
            st.write(f"😐 ニュートラル: {avg_neutral:.1f}%")

            st.divider()

            st.subheader("📈 感情の推移")
            df = pd.DataFrame(
                {
                    "会話番号": range(1, len(user_messages) + 1),
                    "ポジティブ": [m["scores"]["positive"] for m in user_messages],
                    "ネガティブ": [m["scores"]["negative"] for m in user_messages],
                    "ニュートラル": [m["scores"]["neutral"] for m in user_messages],
                }
            )
            st.line_chart(df.set_index("会話番号"))

            st.divider()

            st.subheader("🎨 感情の割合")
            emotion_counts = {
                "ポジティブ": sum(
                    1 for m in user_messages if m.get("emotion") == "ポジティブ"
                ),
                "ネガティブ": sum(
                    1 for m in user_messages if m.get("emotion") == "ネガティブ"
                ),
                "ニュートラル": sum(
                    1 for m in user_messages if m.get("emotion") == "ニュートラル"
                ),
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

            csv_data = []
            for i, m in enumerate(user_messages, 1):
                csv_data.append(
                    {
                        "会話番号": i,
                        "メッセージ": m["content"],
                        "ポジティブ(%)": m["scores"]["positive"],
                        "ネガティブ(%)": m["scores"]["negative"],
                        "ニュートラル(%)": m["scores"]["neutral"],
                        "主な感情": m["emotion"],
                    }
                )
            df_csv = pd.DataFrame(csv_data)
            csv = df_csv.to_csv(index=False).encode("utf-8-sig")

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
