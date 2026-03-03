import random


def mock_openai_response(user_message):
    responses = {
        "ポジティブ": [
            "いいね！その調子だよ！",
            "最高じゃん！",
            "それ、めっちゃいいね！",
        ],
        "ネガティブ": [
            "辛いことがあったんですね。大変でしたね。",
            "その気持ち、わかります。無理しないでくださいね。",
            "大変な時期ですね。少しでも楽になりますように。",
        ],
        "ニュートラル": [
            "なるほど、そうなんですね。",
            "了解しました。",
            "そういうこともありますよね。",
        ],
    }

    positive_words = [
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
    negative_words = [
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

    positive_score = sum(15 for word in positive_words if word in user_message)
    negative_score = sum(15 for word in negative_words if word in user_message)
    neutral_score = 100 - positive_score - negative_score

    if neutral_score < 0:
        neutral_score = 0
        total = positive_score + negative_score
        positive_score = int(positive_score * 100 / total)
        negative_score = 100 - positive_score

    if positive_score > negative_score:
        emotion = "ポジティブ"
    elif negative_score > positive_score:
        emotion = "ネガティブ"
    else:
        emotion = "ニュートラル"

    return {
        "positive": positive_score,
        "negative": negative_score,
        "neutral": neutral_score,
        "response": random.choice(responses[emotion]),
    }


print("=" * 50)
print("  感情分析チャットボット（モック版）")
print("=" * 50)
print("メッセージを入力してください (終了: 'quit')\n")

while True:
    user_input = input("あなた: ").strip()

    if user_input.lower() in ["quit", "exit", "終了"]:
        print("さようなら！")
        break

    if not user_input:
        continue

    result = mock_openai_response(user_input)

    print(f"\n😊 ポジティブ: {result['positive']}%")
    print(f"😢 ネガティブ: {result['negative']}%")
    print(f"😐 ニュートラル: {result['neutral']}%")

    if result["positive"] >= 30:
        print("🎯 主な感情: ポジティブ")
    elif result["negative"] >= 30:
        print("🎯 主な感情: ネガティブ")
    else:
        scores = {
            "ポジティブ": result["positive"],
            "ネガティブ": result["negative"],
            "ニュートラル": result["neutral"],
        }
        dominant = max(scores, key=scores.get)
        print(f"🎯 主な感情: {dominant}")

    print(f"\nボット: {result['response']} 😊\n")
    print("-" * 50 + "\n")
