import os, json

from icrawler import ImageDownloader
from icrawler.builtin import GoogleImageCrawler



def get_languages():
    # Read the JSON file
    with open('language-codes_json.json', 'r') as json_file:
        data = json.load(json_file)

    result = dict()
    for d in data:
        result[d['English']] = d['alpha2']

    # ADD YOUR CODE HERE
    # SEE THE src/language-codes_json.json TO FIND YOUR LANGUAGE
    common_lang = [
        'ar',
        'de',
        'es',
        'fr',
        'en',
        'it',
        'nl',
        'ja',
        'pl',
        'pt',
        'ko',
        'ru',
        'sv',
        'uk',
        'vi',
        'zh'
    ]

    result = {k: v for k, v in result.items() if v in common_lang}

    return result

def get_image_from_google(search_text, save_path='', color='color', max_num=1000):
    """
    :param color: filter option "color" must be one of the following:
    color, blackandwhite, transparent, red, orange, yellow, green, teal, blue, purple, pink, white, gray, black, brown
    """
    save_path = save_path if save_path else f'{"_".join(search_text.split())}_train'

    os.makedirs(save_path, exist_ok=True)

    # filters = dict(license='commercial,modify')

    class PrefixNameDownloader(ImageDownloader):
        def get_filename(self, task, default_ext):
            filename = super(PrefixNameDownloader, self).get_filename(
                task, default_ext)
            return '_'.join(search_text.split()) + '_' + filename

        def process_meta(self, task):
            print(f'process_meta {task}')

    google_crawler = GoogleImageCrawler(
        downloader_cls=PrefixNameDownloader,
        parser_threads=2,
        downloader_threads=4,
        storage={'root_dir': save_path})

    # filter option "color" must be one of the following:
    # color, blackandwhite, transparent, red, orange, yellow, green, teal, blue, purple, pink, white, gray, black, brown
    filters = dict(
        color=color,
    )

    google_crawler.session.verify = False

    google_crawler.crawl(search_text,
                         min_size=(256, 256),
                         max_size=None,
                         max_num=max_num,
                         filters=filters)
