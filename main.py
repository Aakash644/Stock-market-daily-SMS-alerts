STOCK_NAME = "SBIN.BSE"
COMPANY_NAME = "SBI"
import random
import requests 
from datetime import date
from datetime import timedelta
from twilio.rest import Client  
api_key_stock="your_stock_api_key"
param_stock={
    "function":"TIME_SERIES_DAILY_ADJUSTED",
    "symbol":STOCK_NAME,
    "apikey":api_key_stock
}  
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
today=date.today()  
stock=requests.get(url=STOCK_ENDPOINT,params=param_stock) 
stock.raise_for_status() 
stock_data=stock.json()  
account_sid="your_acc_sid" 
auth_token="your_auth_token"
try:
    yesterday=today - timedelta(days = 1)  
    day_before_yesterday=today - timedelta(days = 2)
    stock_closing=[closing for closing in stock_data["Time Series (Daily)"]] 
    yesterday_closing=stock_data["Time Series (Daily)"][f"{yesterday}"]["4. close"]  
    day_before_yest_closing=stock_data["Time Series (Daily)"][f"{day_before_yesterday}"]["4. close"]
    diff=abs(float(yesterday_closing)-float(day_before_yest_closing) )
    actual=float(yesterday_closing)-float(day_before_yest_closing) 
    perc_change=(diff/float(day_before_yest_closing))*100  
    if(perc_change>3): 
       news_api_key="your_news_Api_key"
       ## STEP 2: https://newsapi.org/  
       param_news={"q":COMPANY_NAME,
       "from":f"{yesterday}",
       "sortBy":"publishedAt",
       "apiKey":news_api_key
       } 
       low="🔻"
       high="🔺"
       if(actual>0):
          sign=high
       else:
          sign=low
       news=requests.get(url=NEWS_ENDPOINT,params=param_news)
       
       news_data=news.json() 
       i=0  
       news_title=[]
       while(i<3):
          news1=news_data["articles"][i]["title"]
          news_title.append(news1)
          i=i+1 
       news_description=[] 
       j=0
       while(j<3):
          news2=news_data["articles"][j]["description"]
          news_description.append(news2)
          j=j+1  
    
       
       
       client=Client(account_sid,auth_token) 
       rand=random.randint(0,2)

       message=client.messages \
       .create( 
        body=f''' 
        {COMPANY_NAME}: {sign}{int(perc_change)}
        Headline: {news_title[rand] }
        Brief:{news_description[rand]}''',
        from_="your_api_mobile_number" ,
        to="your_mobile_number"
        )
except KeyError:
    
    client=Client(account_sid,auth_token) 

    message=client.messages \
    .create( 
        body=f'''
        Market were closed yesterday .''',
        from_="your_api_mobile_number" ,
        to="your_mobile_number"
    )
