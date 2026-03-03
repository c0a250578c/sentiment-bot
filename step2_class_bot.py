import random


class SentimentBot:
    def __init__(self):
        print("ボットを初期化中...")

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
                "了解しました。 ",
                "そういうこともあるよ。きっと君なら乗り越えられる!",
            ],
        }
        self.score_weight = 15

        print("ボットの準備完了！")

    def analyze(self, message):
        positive_score = sum(
            self.score_weight for word in self.positive_words if word in message
        )
        negative_score = sum(
            self.score_weight for word in self.negative_words if word in message
        )
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

    def generate_response(self, emotion):
        return random.choice(self.responses[emotion])

    def chat(self, message):
        scores = self.analyze(message)
        emotion = self.get_emotion(scores)
        response = self.generate_response(emotion)

        return {"scores": scores, "emotion": emotion, "response": response}


if __name__ == "__main__":
    print("=" * 50)
    print("感情分析チャットボット (クラス版)")
    print("=" * 50)
    print("メッセージを入力してください (終了: 'quit')\n")

    bot = SentimentBot()
    print()

    while True:
        user_input = input("あなた: ").strip()

        if user_input.lower() in ["quit", "exit", "終了"]:
            print("さようなら！")
            break

        if not user_input:
            continue

        result = bot.chat(user_input)

        print(f"\nポジティブ: {result['scores']['positive']}%")
        print(f"ネガティブ: {result['scores']['negative']}%")
        print(f"ニュートラル: {result['scores']['neutral']}%")
        print(f"主な感情: {result['emotion']}")
        print(f"\nボット: {result['response']}\n")
        print("-" * 50 + "\n")
