# Live Streaming for 🍋.markets

This is a small example about using the [live streaming API](https://docs.lemon.markets/live-streaming/overview) from [lemon.markets](https://lemon.markets/) using Python.

This example will implement a basic stock ticker for the command line.

## Quick Start

1. Replace `YOUR-API-KEY` with your actual API key in `main.py`.
2. Install the dependencies using `pip3 install -r requirements.txt`
3. Run the code: `python main.py`

You should see something like this:

```
Fetching credentials for live streaming…
Fetched.     Token expires at 2022-07-13T02:00:00.020000
             Connecting MQTT client…
Connected.   Subscribing to usr_qyJDQss5546j0bXjtWtLlRC3B4CNBdmg9V…
Subscribed.  Publishing requested instruments to usr_qyJDQss5546j0bXjtWtLlRC3B4CNBdmg9V.subscriptions…
Published.   Fetching latest quotes for initialization…
Initialized. Waiting for live stream messages…
US0378331005(ask=144.6000,bid=144.5400,date=2022-07-12T14:27:15.809) US88160R1014(ask=701.9000,bid=701.0000,date=2022-07-12T14:27:16.261) ⏐
```

If you pay close attention, you will notice updates to the data in the
bottom line as your code receives new updates.
