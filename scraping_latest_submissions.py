import argparse
import json
import os
import praw
from reddit_scraper.utils import unixtime_to_datetime
from reddit_scraper.scraper import yield_submission_from


def save(json_obj, directory):
    filepath = '{}/{}.json'.format(directory, json_obj['id'])
    with open(filepath, 'w', encoding='utf-8') as fp:
        json.dump(json_obj, fp, indent=2, ensure_ascii=False)

def scraping(reddit, begin_date, r, dist, max_num, sleep, directory, verbose, begin_id=None):

    n_exceptions = 0

    for i, json_obj in enumerate(yield_submission_from(reddit, begin_date, r, dist, max_num, sleep)):
        try:
            save(json_obj, directory)
        except Exception as e:
            n_exceptions += 1
            print(e)
            continue

        if verbose:
            title = json_obj['title']
            created_utc = unixtime_to_datetime(json_obj['created_utc'])
            print('[{} / {}] ({}) {}'.format(i+1, max_num, created_utc, title))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--begin_date', type=str, default='2019-01-01_00-00-00', help='datetime YYYY-mm-dd_HH-MM-SS')
    parser.add_argument('--directory', type=str, default='./output/', help='Output directory')
    parser.add_argument('--r', type=str, default='MachineLearning', help='Reddit topic')
    parser.add_argument('--dist', type=str, default='25', help='Dist value corresponding r')
    parser.add_argument('--max_num', type=int, default=100, help='Maximum number of submissions to be scraped')
    parser.add_argument('--sleep', type=float, default=1.0, help='Sleep time for each submission (post)')
    parser.add_argument('--begin_id', type=str, default=None, help='Dist value corresponding r')
    parser.add_argument('--verbose', dest='VERBOSE', action='store_true')

    args = parser.parse_args()
    begin_date = args.begin_date
    directory = args.directory
    r = args.r
    dist = args.dist
    max_num = args.max_num
    sleep = args.sleep
    begin_id = args.begin_id
    VERBOSE = args.VERBOSE

    # load configuration
    with open('./config.json', encoding='utf-8') as f:
        config = json.load(f)

    client_id = config['client_id']
    client_secret = config['client_secret']
    user_agent = config['user_agent']
    username = config['username']
    password = config['password']

    # create Reddit instance
    reddit = praw.Reddit(
        client_id = client_id,
        client_secret = client_secret,
        user_agent = user_agent,
        username = username,
        password = password
    )

    # check output directory
    directory = '{}/{}'.format(directory, r)
    if not os.path.exists(directory):
        os.makedirs(directory)

    scraping(reddit, begin_date, r, dist, max_num, sleep, directory, VERBOSE, begin_id)

if __name__ == '__main__':
    main()