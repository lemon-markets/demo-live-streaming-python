from datetime import datetime
import json
from lemon import api
from lemon.market_data.model.quote import Quote
import paho.mqtt.client as mqtt
import sys

## Configuration

# Your market data API key: https://docs.lemon.markets/authentication
api_key = "YOUR-API-KEY"

instruments = [
    "US0378331005", # Apple
    "US88160R1014", # Tesla
]

## Quotes

quotes = {}
updates = 0
# ⎯ ⟍ ⏐ ⟋
spinner = u"\u23af\u27cd\u23d0\u27cb"

def print_quotes():
    print("\r", end="")
    for instrument in instruments:
        ask = format(quotes[instrument].a / 10000, ".4f")
        bid = format(quotes[instrument].b / 10000, ".4f")
        date = datetime.fromtimestamp(quotes[instrument].t / 1000.0).isoformat(timespec='milliseconds')
        print(f"{instrument}(ask={ask},bid={bid},date={date})", end=" ")
    print(spinner[updates % len(spinner)], end="")
    sys.stdout.flush()

## Lemon Markets API Client

lm_client = api.create(market_data_api_token=api_key, trading_api_token="trading-api-is-not-used")

## Live Streaming Callbacks

def on_connect(mqtt_client, userdata, flags, rc):
    print(f"Connected.   Subscribing to {user_id}…")
    mqtt_client.subscribe(user_id)
    
def on_subscribe(mqtt_client, userdata, level, buff):
    print(f"Subscribed.  Publishing requested instruments to {user_id}.subscriptions…")
    mqtt_client.publish(f"{user_id}.subscriptions", ",".join(instruments))
    # This is a great place to fetch `/v1/quotes/latest` on time via REST, so
    # you have _all_ the latest quotes and you can update them via incoming
    # live stream messages.
    print("Published.   Fetching latest quotes for initialization…")
    latest = lm_client.market_data.quotes.get_latest(isin=instruments, epoch=True, decimals=False)
    for quote in latest.results:
        quotes[quote.isin] = quote
    print("Initialized. Waiting for live stream messages…")
    print_quotes()

def on_message(client, userdata, msg):
    global updates
    data = json.loads(msg.payload)
    quote = Quote._from_data(data, int, int)
    quotes[quote.isin] = quote
    updates += 1
    print_quotes()

## Request Live Streaming Credentials

print("Fetching credentials for live streaming…")

response = lm_client.market_data.post("https://realtime.lemon.markets/v1/auth", json={}).json()
# **NOTE:** Use `expires_at` to reconnect, because this connection will stop
# receiving data.
expires_at = datetime.fromtimestamp(response['expires_at'] / 1000)
print(f"Fetched.     Token expires at {expires_at.isoformat()}")
user_id = response['user_id']
token = response['token']

## Prepare Live Streaming Connection

mqtt_client = mqtt.Client("Ably_Client")
mqtt_client.username_pw_set(username=token)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.on_subscribe = on_subscribe

## Connect

print("             Connecting MQTT client…")
mqtt_client.connect("mqtt.ably.io")
mqtt_client.loop_forever()
