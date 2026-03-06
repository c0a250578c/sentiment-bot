import random
import os
from dotenv import load_dotenv
from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.exceptions import InvalidSignatureError

load_dotenv()

app = Flask(__name__)

CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


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
        self.score_weight = 15

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
        if scores["positive"] >= 30:
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

    def chat(self, message):
        scores = self.analyze(message)
        emotion = self.get_emotion(scores)
        response = random.choice(self.responses[emotion])
        return scores, emotion, response


bot = SentimentBot()


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_message = event.message.text
    scores, emotion, response = bot.chat(user_message)

    reply_text = (
        f"【感情分析結果】\n"
        f"😊 ポジティブ: {scores['positive']}%\n"
        f"😢 ネガティブ: {scores['negative']}%\n"
        f"😐 ニュートラル: {scores['neutral']}%\n"
        f"🎯 主な感情: {emotion}\n\n"
        f"💬 {response}"
    )

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_text)],
            )
        )


if __name__ == "__main__":
    app.run(port=5000, debug=True)
