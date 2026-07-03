import requests
import json
import time


url = "https://w-tid.jp/tokyu/toyoko.json"

data = requests.get(url).json()

print(json.dumps(data, indent=2, ensure_ascii=False))
import requests

# ======================
# 設定
# ======================
JSON_URL = "https://w-tid.jp/tokyu/toyoko.json"
WEBHOOK_URL = "https://discord.com/api/webhooks/1522646800459239484/WGGk1Eh3_rMcc9Sq4bcPrSXA_KJd1us-ZvC70BCVkDgDS9LUN1PQu6wB5r93OhMw8d7d"

sent = set()


def find_trains(obj):
    """
    JSON内から
    kind == '回'
    の辞書をすべて探す
    """

    if isinstance(obj, dict):

        if obj.get("kind") == "回":
            yield obj

        for value in obj.values():
            yield from find_trains(value)

    elif isinstance(obj, list):

        for item in obj:
            yield from find_trains(item)


while True:

    try:

        data = requests.get(JSON_URL, timeout=10).json()

        for train in find_trains(data):

            operation = train.get("operation_number")

            if operation is None:
                continue

            if operation not in sent:

                message = {
                    "content": f"回送列車が走行中です\n運行番号：{operation}"
                }

                requests.post(WEBHOOK_URL, json=message)

                print("通知:", operation)

                sent.add(operation)

    except Exception as e:
        print(e)
    time.sleep(5)