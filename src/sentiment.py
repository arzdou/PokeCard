from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np
from googletrans import Translator
import pandas as pd
import re


def extract_info(api, user):
    tweets = api.user_timeline(screen_name=user.screen_name,
                               count=200,
                               include_rts=True,
                               tweet_mode="extended"
                               )
    out_tweets = [[t.created_at, clean_text(t.full_text)]
                  for t in tweets if t.lang == 'es']

    df = pd.DataFrame(out_tweets, columns=["creation", "text_original"])

    translator = Translator()
    df["text"] = df["text_original"].apply(lambda t: translator.translate(t, src='es').text)

    analyzer = SentimentIntensityAnalyzer()
    df["sentiment"] = df["text"].apply(lambda t: analyzer.polarity_scores(t)['compound'])

    p = (df["sentiment"].to_numpy() > 0).sum()
    n = (df["sentiment"].to_numpy() < 0).sum()

    df.to_csv("test.csv", encoding='utf-8')
    return p, n, len(tweets)


def clean_text(text):
    text = re.sub(r'@[A-Za-z0-9_]+', '', text)
    text = re.sub(r'#', '', text)
    text = re.sub(r'RT[\s]+', '', text)
    text = re.sub(r'https?:\/\/\S+', '', text)
    text = text.lower()
    return text


def analyze_image(image):
    pix = np.array(image).astype(int)
    rgb = pix.reshape(pix.shape[0] * pix.shape[1], 3).T
    color, counts = recursive_color(rgb)
    return color, counts


def recursive_color(pix, bandwidth=5, smooth=True):
    # Create a histogram representation of the pixels in the first color band and smooth it
    _y, _x = np.histogram(pix[0], bins='auto')
    x = np.array([(_x[i]+_x[i+1])/2 for i in range(len(_x)-1)])
    if smooth:
        s = np.ones(len(x)//7+1) / (len(x)//7+1)
        y = np.convolve(_y, s, mode='same')
    else:
        y = _y.copy()

    # Find the index of the maxima in the histogram. If no maxima then take the maximum value
    maxima_idx = np.nonzero(np.r_[True, y[1:] >= y[:-1]+1] & np.r_[y[:-1] >= y[1:]+1, True])[0]
    if not list(maxima_idx):
        maxima_idx = [np.argmax(y)]

    # If we only have one color band end recursion and return maxima
    if pix.shape[0] == 1:
        color = [[int(x[m])] for m in maxima_idx]
        counts = [y[m] for m in maxima_idx]
        return color, counts

    color, counts = [], []
    for m_idx in maxima_idx:
        # For each maxima found filter the pixels of the other bands that do not correspond to that maxima
        # and create a recursion with those filtered sub_bands
        bool_m_idx = (x[m_idx] > pix[0] - bandwidth) * (x[m_idx] < pix[0] + bandwidth)
        new_pix = np.array([c[bool_m_idx] for c in pix[1:]])
        if not list(new_pix[0]): continue
        sub_color, sub_counts = recursive_color(new_pix, bandwidth=bandwidth)
        # Save the found maxima of the other bands within the maxima of the previous band
        for m, c in zip(sub_color, sub_counts):
            m.insert(0, int(x[m_idx]))
            color.append(m)
            counts.append(c)

    return color, counts
