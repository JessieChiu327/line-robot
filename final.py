# coding=UTF-8
from flask import Flask, request, abort,render_template
from bs4 import BeautifulSoup
import requests
from selenium import webdriver


from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('6+yFbPwN3NQnu7adgEmZp/642lN9Bt2sgD2V9oS56qIfeTxARTGu8CXkIfHShp4UU1qdP3D6eeYNx7fHBjIDyJs/etr4UhCsCpW9AT0kYfpbPhAfgxJcffXL9rSKt18IdEhX/POgk0bf40we+JNSGgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a28eea956773ed3a5ebfd9d35d5b19f0')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event.message.text)

    def taxi(meter):
        if meter<=1250:
            money=70
        else:
            money=70+((meter-1250)/200)*5
        return money


    def uber(meter,minute):
        money=40
        money =money+minute*2.5
        if meter<=15000:
            money=money+(meter/1000)*12.5
        else:
            money=money+15*12.5+((meter/1000)-15)*25
        return money

    if event.message.text.split(' ')[0] == "請問今天氣溫":
        import requests		#將套件匯入
        isSupport='是'
        location=event.message.text.split(' ')[1]
        if location =='台北市'and location=='臺北市'and location=='臺北':
            url = 'https://tw.news.yahoo.com/weather/%E8%87%BA%E7%81%A3/%E8%87%BA%E5%8C%97%E5%B8%82/%E8%87%BA%E5%8C%97%E5%B8%82-2306179'    #要下載的檔案或網站來源
        elif location =='新北市':
            url='https://tw.news.yahoo.com/weather/臺灣/新北市/新北市-20070569'
        elif location =='基隆市':
            url='https://tw.news.yahoo.com/weather/臺灣/基隆市/基隆市-2306188'
        elif location =='桃園市':
            url='https://tw.news.yahoo.com/weather/臺灣/桃園市/桃園市-2298866'
        elif location =='新竹市':
            url='https://tw.news.yahoo.com/weather/臺灣/新竹市/新竹市-2306185'
        elif location =='苗栗市':
            url='https://tw.news.yahoo.com/weather/臺灣/苗栗市/苗栗市-2301128'
        elif location =='臺中市'and location=='台中市':
            url='https://tw.news.yahoo.com/weather/臺灣/臺中市/臺中市-2306181'
        elif location =='彰化市':
            url='https://tw.news.yahoo.com/weather/臺灣/彰化市/彰化市-2306183'
        elif location =='南投市':
            url='https://tw.news.yahoo.com/weather/臺灣/南投市/南投市-2306204'
        elif location =='雲林市':
            url='https://tw.news.yahoo.com/weather/臺灣/雲林/雲林-2347346'
        elif location =='嘉義市':
            url='https://tw.news.yahoo.com/weather/臺灣/嘉義市/嘉義市-2296315'
        elif location =='臺南市':
            url='https://tw.news.yahoo.com/weather/臺灣/臺南市/臺南市-2306182'
        elif location =='高雄市':
            url='https://tw.news.yahoo.com/weather/臺灣/高雄市/高雄市-2306180'
        elif location =='屏東市':
            url='https://tw.news.yahoo.com/weather/臺灣/屏東市/屏東市-2306189'
        elif location =='宜蘭市':
            url='https://tw.news.yahoo.com/weather/臺灣/宜蘭市/宜蘭市-2306198'
        elif location =='花蓮市':
            url='https://tw.news.yahoo.com/weather/臺灣/花蓮市/花蓮市-2306187'
        elif location=='台東市'and location=='臺東市':
            url='https://tw.news.yahoo.com/weather/臺灣/臺東市/臺東市-2306190'
        else:
            isSupport='否'
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='不支援此城市'))
        
        
        
        
        if isSupport=='是':       
            r = requests.get(url)	#這一行執行就會下載
            print(r.status_code)	#如果下載成功r.status_code會是int的200
            html = r.text		#r.text就是下載回來的檔案內容

            from bs4 import BeautifulSoup		#匯入套件
            sp = BeautifulSoup(html, 'html.parser')	#將html的文字檔丟進bs4的分析器，並指定使用html.parser的函式庫

            a= sp.find("span",class_="Va(t)")
            print(a.text)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=a.text))
    elif event.message.text=='help':
        replymsg='你可以問我：\n今天氣溫？\n我的名字？\n我的大頭貼？\n我的個簽？\n請問車資 出發地地址 目的地地址'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=replymsg))
    elif event.message.text=='我的名字？':
        profile = line_bot_api.get_profile(event.source.user_id)

        print(profile.display_name)
        print(profile.user_id)
        print(profile.picture_url)
        print(profile.status_message)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=profile.display_name))
    elif event.message.text=='我的大頭貼？':
        profile = line_bot_api.get_profile(event.source.user_id)

        print(profile.display_name)
        print(profile.user_id)
        print(profile.picture_url)
        print(profile.status_message)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=profile.picture_url))
    elif event.message.text=='我的個簽？':
        profile = line_bot_api.get_profile(event.source.user_id)

        print(profile.display_name)
        print(profile.user_id)
        print(profile.picture_url)
        print(profile.status_message)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=profile.status_message))

    elif event.message.text.split(' ')[0] == "請問車資":
        a=event.message.text.split(' ')
        def taxi(meter):
            if meter<=1250:
                money=70
            else:
                money=70+((meter-1250)/200)*5
            return money


        def uber(meter,minute):
            money=40
            money =money+minute*2.5
            if meter<=15000:
                money=money+(meter/1000)*12.5
            else:
                money=money+15*12.5+((meter/1000)-15)*25
            return money

        import requests
        import json
        de = a[1]
        ar = a[2]
        r = requests.get('https://maps.googleapis.com/maps/api/directions/json?origin='+de+'&destination='+ar+'&key=AIzaSyD8OPsqkZeN9bc0AZhPrcBqd0QIoNFdY_w')
        result = json.loads(r.text)
        distance=result["routes"][0]["legs"][0]["distance"]['value']
        time_second=result["routes"][0]["legs"][0]["duration"]['value']

        uber_money=uber(distance,time_second/60)
        print('搭uber的錢：',uber_money)

        taxi_money=taxi(distance)
        print('搭taxi的錢：',taxi_money)
        replyMsg = '預計車程'+str(int(time_second/60))+'分'+'\n搭uber：'+str(int(uber_money))+'元'+'\n搭taxi：'+str(int(taxi_money))+'元'+'\n(僅供參考)\n實際價格會依路況、天氣或其他因素而有所不同'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=replyMsg))
    elif event.message.text.split(' ')[0] == "火車誤點":
        train_no= event.message.text.split(' ')[1]
        import requests
        url='https://train.meshow.info/Home/Delay'
        r = requests.get(url)	#這一行執行就會下載
        print(r.status_code)	#如果下載成功r.status_code會是int的200
        html = r.text		#r.text就是下載回來的檔案內容

        from bs4 import BeautifulSoup		#匯入套件
        sp = BeautifulSoup(html, 'html.parser')	
        table=sp.find_all('tr')
        
        Flag='沒找到'
        for tr in table:
            list1 = tr.text.split('\n')
            car = list1[1]
            if train_no==car:
                Flag='有找到'
                delay = list1[5]
                replymsg='車次'+car+'延誤'+delay
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=replymsg))
        if Flag=='沒找到':
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='此車次沒有延誤'))
    
    
    
    
    
    
    else:
        replymsg1='我不太明白你的意思\n但你可以問我：\n1.請問今天氣溫？\n2.我的名字？\n3.我的大頭貼？\n4.我的個簽？\n5.請問車資 出發地地址 目的地地址'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=replymsg1))


@app.route('/')
def home():
  return render_template('index.html')


@app.route('/test')
def homes():
  return """123"""

if __name__ == "__main__":
    app.run()


