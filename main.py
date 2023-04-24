from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import http.client, urllib, json

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_weather1():
  conn = http.client.HTTPSConnection('apis.tianapi.com')  #接口域名
  params = urllib.parse.urlencode({'key':'3526e085d83b2685f2610ab7ab02c324','city':'101250101','type':'1'})
  headers = {'Content-type':'application/x-www-form-urlencoded'}
  conn.request('POST','/tianqi/index',params,headers)
  tianapi = conn.getresponse()
  result = tianapi.read()
  data = result.decode('utf-8')
  dict_data = json.loads(data)
  weather = dict_data['result']['weather']
  lowest = dict_data['result']['lowest']
  highest = dict_data['result']['highest']
  date = dict_data['result']['date']
  week = dict_data['result']['week']
  tips = dict_data['result']['tips']
  area = dict_data['result']['area']
  return weather, lowest, highest, date, week, tips, area

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

def get_star():
    conn = http.client.HTTPSConnection('apis.tianapi.com')  # 接口域名
    params = urllib.parse.urlencode({'key': '3526e085d83b2685f2610ab7ab02c324', 'astro': 'libra'})
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    conn.request('POST', '/star/index', params, headers)
    tianapi = conn.getresponse()
    result = tianapi.read()
    data = result.decode('utf-8')
    dict_data = json.loads(data)
    color = dict_data['result']['list'][5]['content']
    number = dict_data['result']['list'][6]['content']
    star_result = dict_data['result']['list'][8]['content']
    return color, number, star_result

client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
# wea, temperature = get_weather()
wea, low, high, date_now, week, tips, area = get_weather1()
color, number, star_result = get_star()
data = {"weather":{"value":wea},"low":{"value":low},"high":{"value":high} ,"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
###
URL = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=3c35e930-5284-4f0d-a531-9c813b222e0b'
mHeader = {'Content-Type': 'application/json; charset=UTF-8'}
time = datetime.now()
time_content = "📅今天是{}，{}\n".format(date_now, week)
weather_content = "{}今天天气为{}\n温度最高{}，最低{}\n🎈给婷婷的天气小tips：{}\n".format(area,wea,high,low,tips)
meet_content = "💌今天是我们在一起的第{}天\n".format(get_count())
birthday_content = "/:cake距离婷婷的生日还有{}天\n".format(get_birthday())
star_content = "幸运颜色：{}\n幸运数字：{}\n今日概述：{}\n".format(color,number,star_result)
words = get_words()
weather_x = "********天气播报☁********\n"
important_x = "********重要时间/:heart********\n"
star_x = "********星座运势♎********\n"
content = "/:sun早上好呀婷婷宝贝！\n"+time_content+weather_x+weather_content+important_x+meet_content+birthday_content+star_x+star_content+"\n"+words+"/:rose"
mBody = {
    "msgtype": "text",
    "text": {
        "content": content
    }
}
requests.post(url=URL, json=mBody, headers=mHeader)
###
print(res)
