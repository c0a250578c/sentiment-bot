import pytest
from step4_line_bot import SentimentBot

bot = SentimentBot()


class TestAnalyze:
    def test_positive_basic(self):
        "基本的なポジティブ判定"
        scores = bot.analyze("今日は楽しかった")
        assert scores["positive"] > 0

    def test_negative_basic(self):
        "基本的なネガティブ判定"
        scores = bot.analyze("今日は疲れた")
        assert scores["negative"] > 0

    def test_neutral_basic(self):
        "ニュートラル判定"
        scores = bot.analyze("今日は普通だった")
        assert scores["neutral"] == 100

    def test_negation_positive(self):
        "否定形: 楽しくない → ネガティブ"
        scores = bot.analyze("楽しくない")
        assert scores["negative"] > scores["positive"]

    def test_negation_negative(self):
        "否定形: 疲れていない → ポジティブ"
        scores = bot.analyze("疲れていない")
        assert scores["positive"] > scores["negative"]

    def test_total_is_100(self):
        "スコアの合計が100になる"
        scores = bot.analyze("今日は最高に楽しかった")
        assert scores["positive"] + scores["negative"] + scores["neutral"] == 100

    def test_message(self):
        "空文字はニュートラル"
        scores = bot.analyze("")
        assert scores["neutral"] == 100

    class TestGetEmotion:
        def test_positive_emotion(self):
            "ポジティブ判定"
            scores = {"positive": 60, "negative": 0, "neutral": 40}
            assert bot.get_emotion(scores) == "ポジティブ"

        def test_negative_emotion(self):
            "ネガティブ判定"
            scores = {"positive": 0, "negative": 60, "neutral": 40}
            assert bot.get_emotion(scores) == "ネガティブ"

        def test_neutral_emotion(self):
            "ニュートラル判定"
            scores = {"positive": 0, "negative": 0, "neutral": 100}
            assert bot.get_emotion(scores) == "ニュートラル"

        def test_tie_goes_to_negative(self):
            "同点ネガティブ優先"
            scores = {"positive": 30, "negative": 30, "neutral": 40}
            assert bot.get_emotion(scores) == "ネガティブ"

        class TestChat:
            def test_chat_returns_keys(self):
                "chatメソッドが必要なキーを返す"
                result = bot.chat("今日は楽しかった")
                assert "scores" in result or isinstance(result, tuple)

            def test_chat_positive_response(self):
                "ポジティブなメッセージにポジティブな返答"
                scores, emotion, response = bot.chat("最高に楽しい")
                assert emotion == "ポジティブ"
                assert response in bot.responses["ポジティブ"]
