# Reddit scraper

It scraps the latest submission in the given subreddit (topic).

## Usage

First, set your configuration in `config.json`

```python
begin_date = '2019-01-12 05-12-00'
r = 'MachineLearning'
dist = 25
max_num = 100

for i, json_obj in enumerate(yield_submission_from(begin_date, r, dist, max_num, sleep=1)):
    title = json_obj['title']
    created_utc = unixtime_to_datetime(json_obj['created_utc'])
    print('[{} / {}] ({}) {}'.format(i, max_num, created_utc, title))
```

result

```
[1 / 100] (2019-01-14 03:18:59) [P] Looking for a Model That Has Been Pre-Trained on the ADE20K Dataset
[2 / 100] (2019-01-14 01:53:07) [D] Machine Learning people, What are some things that you struggled learning when you were first starting out?
[3 / 100] (2019-01-13 21:50:23) [D] What are some the labs that focus on DL/Telecom Industry
[4 / 100] (2019-01-13 21:39:30) [D] What's DCGAN talking about not putting BatchNorm at the last layer of G and first layer of D?
[5 / 100] (2019-01-13 19:47:42) [P] Conditional Deep Convolutional GAN (CDCGAN) Keras implementation
[6 / 100] (2019-01-13 12:43:40) [D] How can I retrieve a mathematical/symbolic representation of the gradient derived by the autograd/autodiff modules in popular tensor frameworks?
[7 / 100] (2019-01-13 12:17:48) [D] Enforcing A Latent Space Prior for 1 vs all Classifiers
[8 / 100] (2019-01-13 12:03:06) [P] ML Alternatives For Causal Inference To Pandas Groupby For High Dimensional Data
[9 / 100] (2019-01-13 05:23:57) [D] MIT Deep Learning Basics: Introduction and Overview
[10 / 100] (2019-01-13 04:33:43) [D] Are external GPUs a worthwhile investment?
[11 / 100] (2019-01-13 01:39:25) [R] Spherical Payoff for Bayesian Networks
[12 / 100] (2019-01-12 23:18:57) [P] Implementing P-adam, novel optimization algorithm for Neural Networks
[13 / 100] (2019-01-12 16:06:32) [D] [R] Benchmark results for FashionMNIST
[14 / 100] (2019-01-12 15:51:28) [D] AI Safety and RL
[15 / 100] (2019-01-12 14:32:32) [D] AMD Vega VII for ML?
[16 / 100] (2019-01-12 14:26:51) [D] How much time do you spend catching up on new papers v/s doing your own research?
[17 / 100] (2019-01-12 12:23:40) [D] Semantic Similarity using Universal Sentence Encoder
[18 / 100] (2019-01-12 10:28:50) [D] GAN for hair style transfer?
[19 / 100] (2019-01-12 09:27:38) [D] Was there any conclusion on GloVe vs Word2vec ? Also in their application to encoding other types of items?
Stop scrapping. 19 / 100 posts was scrapped
The oldest submission has been created after 2019-01-12 05-12-00
```

Using Python script

```
python scraping_latest_submissions.py --begin_date 2017-01-01_00-00-00 --r MachineLearning --max_num 100000 --sleep 0.3 --verbose
```

## Requirements

praw >= 6.0.0 (Reddit Python API)