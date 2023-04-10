# ChatGPT Plugins - Replicate Quickstart

Get a [Replicate](https://replicate.com)  ChatGPT plugin up and running in under 5 minutes using Python. If you do not already have ChatGPT plugin developer access, please [join the waitlist](https://openai.com/waitlist/plugins).

## Setup

To install the required packages for this plugin, run the following command:

```bash
pip install -r requirements.txt
```

Grab your [replicate token](https://replicate.com/account), then to run the plugin, enter the following command:

```bash
export REPLICATE_API_TOKEN=....
python main.py
```

Once the local server is running:

1. Navigate to https://chat.openai.com. 
2. In the Model drop down, select "Plugins" (note, if you don't see it there, you don't have access yet).
3. Select "Plugin store"
4. Select "Develop your own plugin"
5. Enter in `localhost:5003` since this is the URL the server is running on locally, then select "Find manifest file".

The plugin should now be installed and enabled! You can start with a question like "Generate an image of a cow on mars"

## Getting help

If you run into issues or have questions building a chatgpt plugins for replicate, please join the [replicate discord](https://discord.gg/replicate)
