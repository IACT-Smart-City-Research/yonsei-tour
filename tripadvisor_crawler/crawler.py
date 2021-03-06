# 출처 : https://github.com/susanli2016/NLP-with-Python/blob/master/Web%20scraping%20Hilton%20Hawaiian%20Village%20TripAdvisor%20Reviews.py

import requests
from bs4 import BeautifulSoup
import csv
import webbrowser
import io
import pandas as pd

def display(content, filename='output.html'):
    with open(filename, 'wb') as f:
        f.write(content)
        webbrowser.open(filename)

def get_soup(session, url, show=False):
    r = session.get(url)
    if show:
        display(r.content, 'temp.html')
    if r.status_code != 200: # not OK
        print('[get_soup] status code:', r.status_code)
    else:
        return BeautifulSoup(r.text, 'html.parser')

def post_soup(session, url, params, show=False):
    '''Read HTML from server and convert to Soup'''

    r = session.post(url, data=params)

    if show:
        display(r.content, 'temp.html')

    if r.status_code != 200: # not OK
        print('[post_soup] status code:', r.status_code)
    else:
        return BeautifulSoup(r.text, 'html.parser')

def scrape(url, lang='ALL'):

    # create session to keep all cookies (etc.) between requests
    session = requests.Session()

    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0',
    })


    items = parse(session, url + '?filterLang=' + lang)

    return items

def parse(session, url):
    '''Get number of reviews and start getting subpages with reviews'''

    print('[parse] url:', url)

    soup = get_soup(session, url)

    if not soup:
        print('[parse] no soup:', url)
        return

    num_reviews = soup.find('span', class_='count').text # get text
    num_reviews = num_reviews[1:-1] 
    num_reviews = num_reviews.replace(',', '')
    num_reviews = int(num_reviews) # convert text into integer
    print('[parse] num_reviews ALL:', num_reviews)
    
    url_template = url.replace('.html', '-or{}.html')
    print('[parse] url_template:', url_template)

    items = []

    offset = 0

    while(offset <= num_reviews):
        subpage_url = url_template.format(offset)

        subpage_items = parse_reviews(session, subpage_url)

        if not subpage_items:
            break

        items += subpage_items

        if len(subpage_items) < 10:
            break

        offset += 10

    return items

def get_reviews_ids(soup):

    items = soup.find_all('div', attrs={'data-reviewid': True})

    if items:
        reviews_ids = [x.attrs['data-reviewid'] for x in items][::2]
        print('[get_reviews_ids] data-reviewid:', reviews_ids)
        return reviews_ids

def get_more(session, reviews_ids):

    url = 'https://www.tripadvisor.com/OverlayWidgetAjax?Mode=EXPANDED_HOTEL_REVIEWS_RESP&metaReferer=Hotel_Review'

    payload = {
        'reviews': ','.join(reviews_ids), # ie. "577882734,577547902,577300887",
        #'contextChoice': 'DETAIL_HR', # ???
        'widgetChoice': 'EXPANDED_HOTEL_REVIEW_HSX', # ???
        'haveJses': 'earlyRequireDefine,amdearly,global_error,long_lived_global,apg-Hotel_Review,apg-Hotel_Review-in,bootstrap,desktop-rooms-guests-dust-en_US,responsive-calendar-templates-dust-en_US,taevents',
        'haveCsses': 'apg-Hotel_Review-in',
        'Action': 'install',
    }

    soup = post_soup(session, url, payload)

    return soup

def parse_reviews(session, url):
    '''Get all reviews from one page'''

    print('[parse_reviews] url:', url)

    soup = get_soup(session, url)

    if not soup:
        print('[parse_reviews] no soup:', url)
        return


    reviews_ids = get_reviews_ids(soup)
    if not reviews_ids:
        return

    soup = get_more(session, reviews_ids)

    if not soup:
        print('[parse_reviews] no soup:', url)
        return

    items = []

    for idx, review in enumerate(soup.find_all('div', class_='reviewSelector')):

        # 유저 신뢰도
        '''
        badgets = review.find_all('span', class_='badgetext')
        if len(badgets) > 0:
            contributions = badgets[0].text
        else:
            contributions = '0'

        if len(badgets) > 1:
            helpful_vote = badgets[1].text
        else:
            helpful_vote = '0'
        user_loc = review.select_one('div.userLoc strong')
        if user_loc:
            user_loc = user_loc.text
        else:
            user_loc = ''
        '''

        # 평점
        # bubble_rating = review.select_one('span.ui_bubble_rating')['class']
        # bubble_rating = int(bubble_rating[1].split('_')[-1]) // 10

        item = {
            'review_title' : review.find('span', class_='noQuotes').text,
            'review_body': review.find('p', class_='partial_entry').text
            # 리뷰 날짜
            # 'review_date': review.find('span', class_='ratingDate')['title'],
       }

        items.append(item)
        '''
        print('\n--- review ---\n')
        for key,val in item.items():
            print(' ', key, ':', val)
        '''

    print()

    return items

def write_in_csv(items, filename='results.csv',
                  headers=['hotel name', 'review title', 'review body',
                           'review date', 'contributions', 'helpful vote',
                           'user name' , 'user location', 'rating'],
              mode='w'):

    print('--- CSV ---')

    with io.open(filename, mode, encoding="utf-8") as csvfile:
        csv_file = csv.DictWriter(csvfile, headers)

        if mode == 'w':
            csv_file.writeheader()

        csv_file.writerows(items)


start_urls = pd.read_csv('/Users/jaewonheo/Documents/yonsei-tour/tripadvisor_crawler/Seoul_URL.csv')['url'].tolist()
start_urls = start_urls[880:]

headers = ['review_title','review_body']
lang = 'en'

for url in start_urls:

    url = 'https://www.tripadvisor.com'+url
    
    filename = url.split('Reviews-')[1][:-5]

    try:
        df = pd.read_csv('/Users/jaewonheo/Documents/yonsei-tour/tripadvisor_crawler/review/'+filename+'.csv')
        print(filename + 'is already exist.')
        continue
    except:
        pass

    # get all reviews for 'url'
    try:
        items = scrape(url, lang)
    except:
        items = {}

    if not items:
        print('No reviews')
    else:
        # write in CSV
        print('filename:', filename)
        write_in_csv(items, '/Users/jaewonheo/Documents/yonsei-tour/tripadvisor_crawler/review/'+filename + '.csv', headers, mode='w')