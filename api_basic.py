import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("エラー: OPENAI_API_KEYが設定されていません")
    exit(1)
print("APIキーが見つかりました")
print(f"キーの最初の7文字: {api_key[:7]}...")

client = OpenAI(api_key=api_key)

print("\nAIに質問を送信中...")
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "こんにちは！簡単に自己紹介してください。"}
    ]
)

print("\n---AIの返答 ---")
print(response.choices[0].message.content)
print("\n 成功！OpenAI APIが動作しています!")
