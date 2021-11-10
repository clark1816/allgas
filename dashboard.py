import streamlit as st
import pandas as pd
import numpy as np
import requests
import tweepy
import config 
import psycopg2, psycopg2.extras
import plotly.graph_objects as go
import datetime
import yfinance as yf
import cufflinks as cf




auth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET)
auth.set_access_token(config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

connection = psycopg2.connect(host = 'localhost', database='etfdb', user='postgres', password='password', port='5432')
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

option = st.sidebar.selectbox("Which Dashboard?", ('twitter', 'wallstreetbets', 'stocktwits', 'patterns','company info','Go to Streamlit'), 1)

st.header(option)

if option == 'twitter':
    for username in config.TWITTER_USERNAMES:
        user = api.get_user(username)
        tweets = api.user_timeline(username)

        st.subheader(username)
        st.image(user.profile_image_url)
        
        for tweet in tweets:
            if '$' in tweet.text:
                words = tweet.text.split(' ')
                for word in words:
                    if word.startswith('$') and word[1:].isalpha():
                        symbol = word[1:]
                        st.write(symbol)
                        st.write(tweet.text)
                        st.image(f"https://finviz.com/chart.ashx?t={symbol}")

if option == 'company info':
    
# Sidebar
    st.sidebar.subheader('company info')
    start_date = st.sidebar.date_input("Start date", datetime.date(2021, 10, 1))
    end_date = st.sidebar.date_input("End date", datetime.date(2021, 11, 10))


# Retrieving tickers data
    ticker_list = pd.read_csv('https://raw.githubusercontent.com/shilewenuw/get_all_tickers/master/get_all_tickers/tickers.csv')
    tickerSymbol = st.sidebar.selectbox('Stock ticker', ticker_list) # Select ticker symbol
    tickerData = yf.Ticker(tickerSymbol) # Get ticker data
    tickerDf = tickerData.history(period='1d', start=start_date, end=end_date) #get the historical prices for this ticker

# Ticker information
    string_logo = '<img src=%s>' % tickerData.info['logo_url']
    st.markdown(string_logo, unsafe_allow_html=True)

    string_name = tickerData.info['longName']
    st.header('**%s**' % string_name)

    string_summary = tickerData.info['longBusinessSummary']
    st.info(string_summary)

# Ticker data
    st.header('**Ticker data**')
    st.write(tickerDf)

# Stock Chart
    st.header('**Stock Chart**')
    qf=cf.QuantFig(tickerDf,title='First Quant Figure',legend='top',name='GS')
    fig = qf.iplot(asFigure=True)
    st.plotly_chart(fig)


if option == 'stocktwits':
    symbol = st.sidebar.text_input("Symbol", value='AAPL', max_chars=5)

    r = requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json")

    data = r.json()

    for message in data['messages']:
        st.image(message['user']['avatar_url'])
        st.write(message['user']['username'])
        st.write(message['created_at'])
        st.write(message['body'])

if option == 'wallstreetbets':
    num_days = st.sidebar.slider('Number of days', 1, 30, 3)
    
    st.info('Number of times a ticker has been mentioned in wallstreet bets reddit page.')

    cursor.execute("""
        SELECT COUNT(*) AS num_mentions, symbol
        FROM mention JOIN stock ON stock.id = mention.stock_id
        WHERE date(dt) > current_date - interval '%s day'
        GROUP BY stock_id, symbol   
        HAVING COUNT(symbol) > 10
        ORDER BY num_mentions DESC
    """, (num_days,))

    counts = cursor.fetchall()
    for count in counts:
        st.write(count)
    
    cursor.execute("""
        SELECT symbol, message, url, dt
        FROM mention JOIN stock ON stock.id = mention.stock_id
        ORDER BY dt DESC
        LIMIT 100
    """)

    mentions = cursor.fetchall()
    for mention in mentions:
        st.text(mention['dt'])
        st.text(mention['symbol'])
        st.text(mention['message'])
        st.text(mention['url'])

    rows = cursor.fetchall()

    st.write(rows)

if st.button('patterns'):
    st.write("check out this [link](https://candle-pattern-app.herokuapp.com/)")
