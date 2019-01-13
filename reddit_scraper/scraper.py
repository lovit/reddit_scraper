def _parse_comment(comment):
    return {
        'author_fullname': comment.author_fullname,
        'created_utc': comment.created_utc,
        'score': comment.score,
        'body_html': comment.body_html,
        'body': comment.body
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
        'selftext_html': submission.selftext_html
    }