import Queue
import threading
import requests
import redis
from bs4 import BeautifulSoup
import sys
import pickle

from locales import locales

guid = sys.argv[1]
#guid = '6e5405fa-e5cc-4a6c-8e54-3932ab7075c3'
url = 'http://marketplaceedgeservice.windowsphone.com/v8/catalog/apps/{guid}?os=8.0.10521.0&cc={cc}&lang={lang}&moId='

redis = redis.StrictRedis('127.0.0.1', '6379')
redis_prefix = 'wpstore-checker'
redis_key = lambda guid, key: '%s.%s.%s' % (redis_prefix, guid, key)
redis_cache_time = 60 * 15

queue = Queue.Queue()
for locale in locales.iteritems():
    this_request = (locale, url.format(guid=guid, cc=locale[1][0], lang=locale[0]),)
    queue.put(this_request)

alive_threads = 0
def thread_worker(queue):
    global alive_threads, guid
    alive_threads += 1
    while True:
        try:
            this_request = queue.get(False)

            locale = this_request[0]
            url = this_request[1]

            print "requesting %s..." % (locale[0],)
            text = requests.get(url).text

            # remove the BOM by bruteforce
            while not text.startswith('<') and len(text):
                text = text[1:]

            print "got %s!" % (locale[0],)
            soup = BeautifulSoup(text, 'xml')
            result = {}

            # published in this store?
            try:
                result['is_available'] = soup.find('isAvailableInCountry').text
            except:
                result['is_available'] = False

            try:
                result['visibility_status'] = soup.find('visibilityStatus').text
            except:
                result['visibility_status'] = 'Error'

            # get purchase types
            try:
                for child in soup.find('offers').children:
                    if child.find('licenseRight').text == 'Trial':
                        result['trial_available'] = True
                    if child.find('licenseRight').text == 'Purchase':
                        result['price'] = child.find('price').text
                        result['price_currency_code'] = child.find('priceCurrencyCode').text
            except:
                pass # no purchases available

            try:
                result['name'] = soup.find('sortTitle').text
            except:
                result['name'] = '---'
            result['locale_language'] = locale[0]
            result['locale_cc'] = locale[1][0]
            result['locale_longname'] = locale[1][1]
            result['guid'] = guid
            if not 'trial_available' in result:
                result['trial_available'] = False

            key = redis_key(guid, locale[0])
            redis.hmset(key, result)
            print "saved inside %s" % (key,)
            key = redis_key(guid, 'status')
            redis.set(key, 'processing')
            redis.expire(key, redis_cache_time)
        except Queue.Empty:
            alive_threads -= 1
            if not alive_threads:
                key = redis_key(guid, 'status')
                redis.set(key, 'done')
                redis.expire(key, redis_cache_time)
                print "results collected for %s, exiting" % (guid,)
            break
        except: # any other thing.
            raise
            key = redis_key(guid, 'status')
            redis.set(key, 'error')
            redis.expire(key, redis_cache_time)
            print "error for %s" % (guid,)
            sys.exit(1)

key = redis_key(guid, 'status')
redis.set(key, 'processing')
redis.expire(key, redis_cache_time)

max_threads = 5
for i in range(max_threads):
    thread = threading.Thread(target=thread_worker, args=(queue,))
    thread.start()