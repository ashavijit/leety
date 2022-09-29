# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=line-too-long

BOT_NAME ='roots'

SPIDER_MODULES=['roots.spiders']
NEWSPIDER_MODULE='roots.spiders'


USER_AGENT='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'

ROBOTSTXT_OBEY=False

DOWNLOAD_DELAY=0.5

CONCURRENT_REQUESTS_PER_DOMAIN= 8


