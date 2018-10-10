'''

import json, re
JSONP = 'callbackFunction(["customername1","customername2"])'
j = json.loads(re.findall(r'^\w+\((.*)\)$',JSONP)[0])
print(type(j),j)

<class 'list'> ['customername1', 'customername2']



ilehash = re.findall('"FileHash":"(.*?)"',resp.text)[0]
songname = re.findall('"SongName":"(.*?)"',resp.text)[0].replace("<\\/em>","").replace("<em>","")

'''

import requests,re,json

import pymongo


client = pymongo.MongoClient(host='localhost',port=27017)

db = client.spiders

collection = db['test']


def down_song(mp3):
    hash_url = "http://www.kugou.com/yy/index.php?r=play/getdata&callback=jQuery191007401245460459349&hash="+mp3['FileHash']
    res = requests.get(hash_url)
    if res.status_code == 200:
        m = re.search(r'^\w+\((.*?)\);$', res.text, re.DOTALL|re.M)
        mp3_json_string = m.group(1)
        try:
            mp3_json = json.loads(mp3_json_string)
            list = {
                "audio_name": mp3_json['data']['audio_name'],
                "album_name": mp3_json['data']['album_name'],
                "have_mv": mp3_json['data']['have_mv'],
                "img": mp3_json['data']['img'],
                "author_name": mp3_json['data']['author_name'],
                "song_name": mp3_json['data']['song_name'],
                "timelength": mp3_json['data']['timelength'],
                "play_url": mp3_json['data']['play_url']
            }
            return list
        except:
            print('error!')



def main(url):

    resp  = requests.get(url)
    #解析json串
    m=re.search(r'^\w+\((.*?)\)$',resp.text,re.DOTALL|re.M)
    mp3_json_string = m.group(1)
    json_dict = json.loads(mp3_json_string,encoding='utf-8')

    for mp3 in json_dict['data']['lists']:
        song_json = down_song(mp3)
        result1 = collection.insert(song_json)
        if result1:
            print("歌曲:",song_json['audio_name'],"入库成功")



if __name__ == '__main__':
    keyword = input("请输入想要听的歌曲：")
    url = "http://songsearch.kugou.com/song_search_v2?callback=jQuery1124006980366032059648_1518578518932&keyword=" + keyword + "&page=1&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0&_=1518578518934"
    main(url)
