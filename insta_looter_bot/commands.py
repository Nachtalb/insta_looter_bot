import os
import re
import shutil
from uuid import uuid4
import io

from botanio import botan
from instaLooter import InstaLooter
from telegram import Bot, Update
from telegram.parsemode import ParseMode

from .settings import BOTAN_API_TOKEN, INSTA_USERNAME, INSTA_PASSWORD

looter = None


def new_looter(*args, **kwargs):
    """Create a new looter with the given parameters

    Args:
        *args: All the parameters as in :class:`instaLooter.core.InstaLooter`
        **kwargs: All the parameters as in :class:`instaLooter.core.InstaLooter`
    """
    global looter
    looter = InstaLooter(*args, **kwargs)

    if INSTA_USERNAME and INSTA_PASSWORD:
        looter.login(INSTA_USERNAME, INSTA_PASSWORD)


def start(bot: Bot, update: Update):
    """Send Start / Help message to client.

    Args:
        bot (:obj:`telegram.bot.Bot`): Telegram Api Bot Object.
        update (:obj:`telegram.update.Update`): Telegram Api Update Object
    """
    if BOTAN_API_TOKEN:
        botan.track(BOTAN_API_TOKEN, update.message.from_user.id, update.message.to_dict(), '/start')

    reply = ("""*Insta Looter Bot*

[@insta_looter_bot](https://t.me/insta_looter_bot)

*How to use me*
Send me a link to an Instagram post or to an Instagram user. If you send me a post I will send the image or video to 
you. If you send me a user I will send you all his/her posts. Because some user just wont stop posting images, this 
could take some time. I really do recommend to use the post download method and not the user download method.

*Features*
- Download a specific post from a user
- Download all posts from a user

*Commands*
- /help, /start: show a help message with information about the bot and it's usage.
- /request USERNAME: request a private user to be followed.

*Attention whore stuff*
Please share this bot with your friends so that I ([the magician](https://github.com/Nachtalb) behind this project) 
have enough motivation to continue and maintain this bot.

Check out my other project\[s\]: 
- [@animu_image_search_bot](https://github.com/Nachtalb/animu_image_search_bot) - Reverse image search bot for telegram

*Contributions*
_Bug report / Feature request_
If you have found a bug or want a new feature, please make an issue here: [Nachtalb/insta_looter_bot](https://github.com/Nachtalb/insta_looter_bot)

_Code Contribution / Pull Requests_
Please use a line length of 120 characters and [Google Style Python Docstrings](http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).

Thank you for using [@insta_looter_bot](https://t.me/insta_looter_bot).""")

    update.message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)


def download(bot: Bot, update: Update, *args):
    """Parse the sent link and download the images from there

    Args:
        bot (:obj:`telegram.bot.Bot`): Telegram Api Bot Object.
        update (:obj:`telegram.update.Update`): Telegram Api Update Object
    """
    if BOTAN_API_TOKEN:
        botan.track(BOTAN_API_TOKEN, update.message.from_user.id, update.message.to_dict(), '/download')
    image_sent = False
    message_sent = False

    base_url = 'instagram.com'
    sent = update.message.text.strip()
    http_re = re.compile('^((http(s)?:)?//)?(www\.)?')
    sent = http_re.sub('', sent)
    if base_url not in sent:
        message_sent = True
        update.message.reply_text('You have to send me an instagram link')
        return

    path = sent.replace(base_url, '')
    try:
        if path.startswith('/p/'):
            post_token = path.replace('/p/', '').split('?', 1)[0].strip(' /')
            try:
                post = looter.get_post_info(post_token)
                if post['is_video']:
                    video = post.get('video_url', download_to_object(post))
                    bot.send_video(update.message.chat_id, video=video)
                else:
                    bot.send_photo(update.message.chat_id, photo=post['display_src'])
                image_sent = True
            except KeyError:
                message_sent = True
                update.message.reply_text('Could not get image, maybe user is private.')
        else:
            username = path.split('?', 1)[0].strip(' /')
            new_looter(profile=username)
            media_generator = looter.medias(with_pbar=True)
            for index, media in enumerate(media_generator):
                try:
                    if media['is_video']:
                        video = media.get('video_url', download_to_object(media))
                        bot.send_video(update.message.chat_id, video=video)
                    else:
                        bot.send_photo(update.message.chat_id, photo=media['display_src'])
                    image_sent = True
                except KeyError:
                    message_sent = True
                    update.message.reply_text('Could not get image/video number %s.' % (index + 1))
            update.message.reply_text('All images sent! :P')
    except Exception as e:
        message_sent = True
        update.message.reply_text('Could not get requested image[s]')
        raise e

    if not message_sent and not image_sent:
        update.message.reply_text('Could not get requested image[s], maybe the profile is private.')


def download_to_object(media):
    """Download a post to a file like bytes object.

    Args:
        media (:obj:`dict`): A post dictionary given by the instagram api

    Returns:
        File like object of the image or video
    """
    global looter
    post_code = media['code']
    post_id = media['id']
    is_video = media['is_video']

    current_dir = os.path.dirname(os.path.realpath(__file__))
    temp_dir = os.path.join(current_dir, str(uuid4())[:8])
    looter.directory = temp_dir
    if temp_dir is not None and not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    looter.download_post(post_code)
    filename = post_id
    filename += '.mp4' if is_video else '.jpg'
    with open(os.path.join(temp_dir, filename), 'rb') as post_file:
        file_object = io.BytesIO(post_file.read())

    shutil.rmtree(temp_dir)
    return file_object


def request(bot: Bot, update: Update, args: list):
    """Request a private user to be followed

    Args:
        bot (:obj:`telegram.bot.Bot`): Telegram Api Bot Object.
        update (:obj:`telegram.update.Update`): Telegram Api Update Object
        args (:obj:`list`): List of arguments passed by the user. First argument must be set and must be the username
            of a instagramm user
    """
    if BOTAN_API_TOKEN:
        botan.track(BOTAN_API_TOKEN, update.message.from_user.id, update.message.to_dict(), '/login')
    if len(args) < 1:
        update.message.reply_text('Use request like this /request INSTAGRAM_USERNAME')
    current_dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(current_dir, 'requests.txt'), 'a') as request_file:
        request_file.write(args[0])


def unknown(bot: Bot, update: Update):
    """Send a error message to the client if the entered command did not work.

    Args:
        bot (:obj:`telegram.bot.Bot`): Telegram Api Bot Object.
        update (:obj:`telegram.update.Update`): Telegram Api Update Object
    """
    if BOTAN_API_TOKEN:
        botan.track(BOTAN_API_TOKEN, update.message.from_user.id, update.message.to_dict(), 'unknown')
    update.message.reply_text("Sorry, I didn't understand that command.")
