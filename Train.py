import pandas as pd
import codecs, bisect, datetime
from nltk.sentiment import vader

def sentiment(tweet_data, i):

    sia = vader.SentimentIntensityAnalyzer()
    return sia.polarity_scores(tweet_data['Text'][i])['compound']


def compute(tweet_data, start, end):

    if start == end:
        return 0
    temp1 = int(end)-int(start)
    temp2 = 0
    for i in range(start,end+1):
        temp2 += sentiment(tweet_data,i)
    return temp2/temp1


def date_change(str_date):

    if str_date:
        return datetime.datetime.strptime(str_date, '%d-%m-%Y').strftime('%Y-%m-%d')


def viewers_change(str_views):

    if str_views == 'NaN':
        return '0'
    return str(int(float(str_views) * 1000000))


# def date_change(str_date):

#     return datetime.datetime.strptime(str_date, '%B %d, %Y')


# def viewers_change(str_views):

#     return str(int(float(str_views.strip().split('[')[0]) * 1000000))


def main():

    viewer_data = pd.read_csv('simpsons_episodes.csv', index_col=False, usecols=range(13))
    tweet_data = pd.read_csv('tweet-data.csv', index_col=False, usecols=range(12), low_memory = False)
    # tweet_data = pd.read_csv('tweet-data.csv', index_col=False, usecols=range(12) , dtype = {"ID" : str, "Author_ID" : str , "Retweets" : str, "Favorites" : str})

    # tweet_data = tweet_data.sort_values('Date', ascending=True)
    viewer_data['Air_Date'] = list(map(date_change, viewer_data['Air_Date']))
    viewer_data['US_Viewers_In_Millions'] = list(map(viewers_change, viewer_data['US_Viewers_In_Millions']))

    tweet_data['Date'] = list(map(date_change, tweet_data['Date']))
    # viewer_data['Original air date'] = list(map(date_change,viewer_data['Original air date']))
    # viewer_data['U.S. viewers(millions)'] = list(map(viewers_change,viewer_data['U.S. viewers(millions)']))

    first_date = bisect.bisect_left(viewer_data['Air_Date'], '2010-01-01')
    last_date = bisect.bisect_left(viewer_data['Air_Date'], '2016-01-01')

    final_score = list()

    count = 1
    for i in range(first_date, last_date - 1):
        temp1 = str(viewer_data['Air_Date'][i])
        temp2 = str(viewer_data['Air_Date'][i + 1])

        start = bisect.bisect_left(tweet_data['Date'], temp1)
        end = bisect.bisect_left(tweet_data['Date'], temp2)
        temp3 = compute(tweet_data, start, end)

        print(count, temp2, viewer_data['Title'][i + 1], temp3)

        count += 1
        final_score.append(temp3)

        # viewer_data['Score'][i+1] = compute(tweet_data,start,end)

if __name__ == "__main__":

    main()