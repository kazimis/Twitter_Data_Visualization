import json
import nltk
import csv
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import collections
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def remove_url_punc_num(text):
    """Remove URLs,punctuations and numbers from a text string"""
    url_pattern = re.compile(r'http\S+|www\.\S+')
    url_removed = url_pattern.sub(r'',str(text))
    return url_removed.lower()


def check_eng_words(tokens):
    """Remove words whihch are not in NLTK english word dictionary"""
    eng_words = set(nltk.corpus.words.words())
    return [token for token in tokens if token in eng_words]


def remove_stopwords(tokens):
    """Remove stop words"""
    return [token for token in tokens if token not in stopwords.words('english')]


def lemmatizer(tokens):
    """Lemmatize word in list of tokenized words
    ADJ, ADJ_SAT, ADV, NOUN, VERB = 'a', 's', 'r', 'n', 'v'
    """
    lemmatizer = nltk.WordNetLemmatizer()
    pos_list = ['n','v','a','s','r']
    result = tokens
    for p in pos_list:
        result = [lemmatizer.lemmatize(token,pos =p) for token in result]
    return result


def stemmer(tokens):
    """stemmerize token in tokens list"""
    stemmer= nltk.PorterStemmer()
    return [stemmer.stem(token) for token in tokens]


def remove_duplicate(tokens):
    """Remove duplicate word from each tweet"""
    return list(dict.fromkeys(tokens))


def get_color(word, **kwargs):
    """assign color to each word based on frequency"""
    global top_100_normalized
    return "hsl(%d, 60%%, 50%%)" % (1000 * top_100_normalized[word])


def store_freq(dict_data):
    """this function store frequency table in csv file"""
    csv_columns = ['Word','Frequency']
    csv_file = "D1_freq.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(csv_columns)
            for data in dict_data:
                writer.writerow([data,dict_data[data]])
    except IOError:
        print("I/O error")


if __name__ == "__main__":
    df = pd.read_csv("D1.csv",names = ["id","created_at","text"],encoding = "utf-8")

    # call text processing functions
    df["tidy_tweet"] = df['text'].apply(remove_url_punc_num)
    df["tokens"] = df['tidy_tweet'].apply(nltk.wordpunct_tokenize)
    df["tokens"] = df['tokens'].apply(remove_stopwords)
    df["tokens"] = df['tokens'].apply(lemmatizer)
    df["tokens"] = df['tokens'].apply(remove_duplicate)
    df["tokens"] = df['tokens'].apply(check_eng_words)

    # find the statiscal results
    token_list = df['tokens'].explode()
    token_list = token_list.dropna()
    num_unique_token = len(token_list.unique())
    print("number of unique token = ",num_unique_token)
    word_count_dict= nltk.FreqDist(token_list)
    top_100 = word_count_dict.most_common(100)
    top_100_normalized = {dict[0]: dict[1]/1000 for dict in top_100}
    print(top_100_normalized)
    store_freq(top_100_normalized)

    # create word cloud and export to file
    x, y = np.ogrid[:300, :300]
    mask = (x-150) ** 2 + (y-150) ** 2 > 160 ** 2
    mask = 255 * mask.astype(int)
    wordcloud = WordCloud(mask = mask,scale = 2).generate_from_frequencies(top_100_normalized)
    wordcloud.recolor(color_func=get_color,random_state=1)
    wordcloud.to_file('D1_wordcloud.png')

    # create figure of word cloud
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.title('Top 100 most frequent words without keyword')
    plt.axis("off")
    plt.show()
