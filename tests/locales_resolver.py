from bs4 import BeautifulSoup
import requests

locales = (
    ('IN', 'hi-in',),
    ('AO', 'pt-ao',),
    ('AR', 'es-ar',),
    ('AM', 'en-am',),
    ('AU', 'en-au',),
    ('AZ', 'az-latn-az',),
    ('BD', 'en-bd',),
    ('BE', 'nl-be',),
    ('BE', 'fr-be',),
    ('BJ', 'fr-bj',),
    ('BO', 'es-bo',),
    ('BR', 'pt-br',),
    ('BF', 'fr-bf',),
    ('BI', 'fr-bi',),
    ('CM', 'en-cm',),
    ('CA', 'en-ca',),
    ('CA', 'fr-ca',),
    ('CZ', 'cs-cz',),
    ('CL', 'es-cl',),
    ('CO', 'es-co',),
    ('CD', 'fr-cd',),
    ('CR', 'es-cr',),
    ('CI', 'fr-ci',),
    ('DK', 'da-dk',),
    ('DE', 'de-de',),
    ('EC', 'es-ec',),
    ('EE', 'et-ee',),
    ('SV', 'es-sv',),
    ('ES', 'es-es',),
    ('ES', 'ca-es',),
    ('FR', 'fr-fr',),
    ('GH', 'en-gh',),
    ('GT', 'es-gt',),
    ('GN', 'fr-gn',),
    ('HT', 'fr-ht',),
    ('HN', 'es-hn',),
    ('HK', 'en-hk',),
    ('HR', 'hr-hr',),
    ('IS', 'is-is',),
    ('IN', 'en-in',),
    ('ID', 'id-id',),
    ('IE', 'en-ie',),
    ('IT', 'it-it',),
    ('KE', 'en-ke',),
    ('KW', 'en-kw',),
    ('LV', 'lv-lv',),
    ('LI', 'de-li',),
    ('LT', 'lt-lt',),
    ('MG', 'fr-mg',),
    ('HU', 'hu-hu',),
    ('MW', 'en-mw',),
    ('MY', 'ms-my',),
    ('MY', 'en-my',),
    ('ML', 'fr-ml',),
    ('MX', 'es-mx',),
    ('MZ', 'pt-mz',),
    ('NL', 'nl-nl',),
    ('NZ', 'en-nz',),
    ('NI', 'es-ni',),
    ('NE', 'fr-ne',),
    ('NG', 'en-ng',),
    ('NO', 'nb-no',),
    ('AT', 'de-at',),
    ('UZ', 'uz-latn-uz',),
    ('PK', 'en-pk',),
    ('PY', 'es-py',),
    ('PE', 'es-pe',),
    ('PH', 'en-ph',),
    ('PH', 'fil-ph',),
    ('PL', 'pl-pl',),
    ('PT', 'pt-pt',),
    ('DO', 'es-do',),
    ('RO', 'ro-ro',),
    ('RW', 'fr-rw',),
    ('CH', 'de-ch',),
    ('SN', 'fr-sn',),
    ('AL', 'sq-al',),
    ('SL', 'en-sl',),
    ('SG', 'en-sg',),
    ('SI', 'sl-si',),
    ('SK', 'sk-sk',),
    ('SO', 'en-so',),
    ('ZA', 'en-za',),
    ('CS', 'sr-latn-cs',),
    ('CH', 'fr-ch',),
    ('FI', 'fi-fi',),
    ('SE', 'sv-se',),
    ('CH', 'it-ch',),
    ('TZ', 'en-tz',),
    ('TD', 'fr-td',),
    ('TG', 'fr-tg',),
    ('TR', 'tr-tr',),
    ('UG', 'en-ug',),
    ('GB', 'en-gb',),
    ('US', 'en-us',),
    ('VE', 'es-ve',),
    ('VN', 'vi-vn',),
    ('ZM', 'en-zm',),
    ('ZW', 'en-zw',),
    ('GR', 'el-gr',),
    ('BY', 'be-by',),
    ('BG', 'bg-bg',),
    ('KZ', 'kk-kz',),
    ('MK', 'mk-mk',),
    ('RU', 'ru-ru',),
    ('TJ', 'ru-tj',),
    ('TM', 'ru-tm',),
    ('UA', 'uk-ua',),
    ('IL', 'he-il',),
    ('JO', 'ar-jo',),
    ('AE', 'ar-ae',),
    ('BH', 'ar-bh',),
    ('DZ', 'ar-dz',),
    ('IQ', 'ar-iq',),
    ('KW', 'ar-kw',),
    ('MA', 'ar-ma',),
    ('SA', 'ar-sa',),
    ('YE', 'ar-ye',),
    ('TN', 'ar-tn',),
    ('OM', 'ar-om',),
    ('QA', 'ar-qa',),
    ('EG', 'ar-eg',),
    ('TH', 'th-th',),
    ('KR', 'ko-kr',),
    ('CN', 'zh-cn',),
    ('TW', 'zh-tw',),
    ('JP', 'ja-jp',),
    ('HK', 'zh-hk',),
)
url = 'http://www.windowsphone.com/{locale}/store/app/whatsapp/218a0ebb-1585-4c7e-a9ec-054cf4569a79'

markets = {}
for locale in locales:
    r = requests.get(url.format(locale=locale[1]))
    soup = BeautifulSoup(r.text)
    market = soup.find(attrs={'data-ov': 'Footer:Markets'}).text

    markets[market] = (locale[0], locale[1])
    print "Added %s: %s" % (locale[0], market)

with open('locales', 'w') as file:
    file.write(repr(markets))