import json
import math
import praw
import time
import requests
from .utils import get_soup
from .utils import strf_to_datetime
from .utils import unixtime_to_datetime


def _parse_comment(comment):
    return {
        'author_fullname': comment.author_fullname,
        'created_utc': comment.created_utc,
        'score': comment.score,
        'body_html': comment.body_html,
        'body': comment.body,
        'id': comment.id
    }

def parse_submission(submission):
    """
    Usage
    -----
        import praw
        
        reddit = praw.Reddit(
            client_id = 'YOURS',
            client_secret = 'YOURS',
            user_agent = 'YOURS',
            username = 'YOURS',
            password = 'YOURS'
        )
        
        submission = reddit.submission(id='a8yaro')
        submission_json = parse_submission(submission)
    """
    return {
        'title': submission.title,
        'comments': [_parse_comment(comment)
                     for comment in submission.comments],
        'created_utc': submission.created_utc,
        'author_fullname': submission.author_fullname,
        'selftext': submission.selftext,
        'selftext_html': submission.selftext_html,
        'id': submission.id
    }

def parse_idx(strf):
    return strf[3:]

def get_after_submission_ids(r, after_id, dist):
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.reddit.com',
        'referer': 'https://www.reddit.com/r/{}/new/'.format(r),
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    request_base = 'https://gateway.reddit.com/desktopapi/v1/subreddits/{}?rtj=debug&redditWebClient=web2x&app=web2x-client-production&after=t3_{}&dist={}&layout=card&sort=new&allow_over18=&include='
    url = request_base.format(r, after_id, dist)
    r = requests.get(url=url, headers=headers)
    submission_ids = [parse_idx(idx) for idx in json.loads(r.text)['postIds']]
    return submission_ids

def yield_submission_from(reddit, begin_date, r, dist, max_num=100, sleep=1, begin_id=None):
    """
    Arguments
    ---------
    reddit : praw.Reddit
        Reddit instance logged with id & OAuth
    begin_date : str
        Begin date str format. 2018-01-01
    r : str
        Subreddit name. For example, ['MachineLearning', 'Politics']
    d : str or int
        dist idx corresponding r
    max_num : int
        Maximum number of submissions (posts) to be scraped
    sleep : float
        Sleep time for each submission
    begin_id : str
        Submission id, the latest post
        Default is None. If None, this function find begin_id, first.

    It yields
    -----
    submission as json format

    Usage
    -----

        from reddit_scraper import yield_submission_from

        # arguments
        begin_date = '2019-01-12 05-12-00'
        r = 'MachineLearning'
        dist = 25
        max_num = 100
        slee = 1

        for json_obj in yield_submission_from(begin_date, r, dist, max_num, sleep):
            # do something
    """

    d_begin = strf_to_datetime(begin_date)
    # get latest submission idx
    soup = get_soup('https://www.reddit.com/r/{}/new/'.format(r))
    if begin_id is None:
        after_id = soup.select('div[class^=scrollerItem]')[0].attrs['id']
        after_id = parse_idx(after_id)
    else:
        after_id = begin_id

    # set iteration parameters
    n_tries = math.ceil(max_num/25)
    n_posts = 0
    outdate = False

    # iterate
    for _ in range(n_tries):
        # check max_num
        if n_posts >= max_num:
            break

        # check begin date
        if outdate:
            print('Stop scrapping. {} / {} posts was scrapped'.format(n_posts, max_num))
            print('The oldest submission has been created after {}'.format(begin_date))
            break

        # get submission ids
        submission_ids = get_after_submission_ids(r, after_id, dist)

        for idx in submission_ids:
            if n_posts >= max_num:
                break
            submission = reddit.submission(id=idx)

            # check begin date
            created = unixtime_to_datetime(submission.created_utc)
            if d_begin > created:
                outdate = True
                break

            # parse submission and yield the result
            json_obj = parse_submission(submission)
            yield json_obj

            # flush
            n_posts += 1
            after_id = idx
            time.sleep(sleep)
