# Insta Looter Bot

[@insta_looter_bot](https://t.me/insta_looter_bot)

<!-- toc -->

- [How to use me](#how-to-use-me)
- [Features](#features)
- [Commands](#commands)
- [Attention whore stuff](#attention-whore-stuff)
- [Contributions](#contributions)
  * [Bug report / Feature request](#bug-report--feature-request)
  * [Code Contribution / Pull Requests](#code-contribution--pull-requests)
  * [Local installation](#local-installation)

<!-- tocstop -->

## How to use me
Send me a link to an Instagram post or to an Instagram user. If you send me a post I will send the image or video to 
you. If you send me a user I will send you all his/her posts. Because some user just wont stop posting images, this 
could take some time. I really do recommend to use the post download method and not the user download method.

## Features
- Download a specific post from a user
- Download all posts from a user

## Commands
- /help, /start: show a help message with information about the bot and it's usage.
- /request USERNAME: request a private user to be followed.

## Attention whore stuff
Please share this bot with your friends so that I ([the magician](https://github.com/Nachtalb) behind this project) 
have enough motivation to continue and maintain this bot.

Check out my other project\[s\]: 
- [@animu_image_search_bot](https://github.com/Nachtalb/animu_image_search_bot) - Reverse image search bot for telegram

## Contributions
### Bug report / Feature request
If you have found a bug or want a new feature, please make an issue here: [Nachtalb/insta_looter_bot](https://github.com/Nachtalb/insta_looter_bot)

### Code Contribution / Pull Requests
Please use a line length of 120 characters and [Google Style Python Docstrings](http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).

### Local installation
Instead of the old `pip` with `requirements.txt` I use the new and fancy `pipenv` with `pipfile`. If you read the intro
to [pipenv](https://github.com/pypa/pipfile) and [pipfile](https://docs.pipenv.org) you will understand why I use it.

With this info we now install our virtualenv with: 
```bash
pip install pipenv  # Install pipenv
pipenv --three      # Create virtualeenv from your python3 installation
pipenv install      # Install all requirements
pipenv shell        # Spawn shell for your pipenv virtualenv
``` 

After this is complete, you have to get an API Token from Telegram. You can easily get one via the
[@BotFather](https://t.me/BotFather).

Now that you have your API Token copy the `settings.example.py` to `settings.py` and paste in your API Token.
Finally you can use this to start your bot.
```bash
python run_bot.py
``` 

In the `settings.py` you can additionally add a [botan.io](http://botan.io) API Token which let's you create 
statistics. You can also give me some Instagram Credentials, with which the bot signs in on startup to enable insight to
private users. Of course you have to follow these private users to use them. 

Thank you for using [@insta_looter_bot](https://t.me/insta_looter_bot).
