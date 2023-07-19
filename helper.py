from urlextract import URLExtract
import pandas as pd
from collections import Counter
import emoji
from cleantext import clean
import re


def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # fetch number of messages
    num_messages = df.shape[0]

    # fetch number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch number of links
    extractor = URLExtract()
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'percent', 'user': 'Name'})
    return x, df


# def createWordCloud(selected_user, df):
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]
#         wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
#         # df_wc = wc.generate(df['message'].str.cat(sep=" "))
#         corpus = " ".join(df['message'])
#         df_wc = wc.generate(corpus)
#         return df_wc

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + " - " + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    day_timeline = df.groupby("date_num").count()['message'].reset_index()
    return day_timeline


def weekly_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()


def monthly_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()


def periodic_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    user_map = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_map


def remover_utility(input_string):
    pattern = r'@\d+'
    output_string = re.sub(pattern, '', input_string)
    return output_string


def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notifications']
    temp = temp[temp['message'] != '<Media omitted>\n']

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    words = []
    for message in temp['message']:
        message = clean(message, no_emoji=True)
        message = remover_utility(message)
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    df_mc = pd.DataFrame(Counter(words).most_common(20))
    return df_mc


def most_common_emojis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    emojis = []
    emojis.extend([match["emoji"] for message in df['message'] for match in emoji.emoji_list(message)])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(6)).rename(columns={0: 'Emoji', 1: "Count"})
    return emoji_df
