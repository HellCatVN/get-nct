# -*- coding: utf-8 -*-
import requests
import json
from flask import Flask,request, render_template ,jsonify

app = Flask(__name__)

def getID(link):
    link = link.replace("https://www.nhaccuatui.com/bai-hat/", "")
    res=link.split('.')
    if len(res) == 3:
        return res[1]
    else:
        return

def createToken( ):
    url = "https://graph.nhaccuatui.com/v1/commons/token"
    headers={
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "graph.nhaccuatui.com",
        "Connection": "Keep-Alive"
    }
    values ='deviceinfo={"DeviceID":"dd03852ada21ec149103d02f76eb0a04","DeviceName":"HellCatVN:S7:NMF26X","OsName":"ANDROID","OsVersion":"8.0","AppName":"NCTTablet","UserName":"hellcatvn","QualityPlay":"128","QualityDownload":"128","QualityCloud":"128","Network":"WIFI","Provider":"NCTCorp"}&md5=ebd547335f855f3e4f7136f92ccc6955&timestamp=1499177482892'
    req = requests.post(url, data=values, headers=headers)
    data =json.loads(req.text)
    token = data['data']['accessToken']
    return token

def songJson(id,token):
    linklist = 'https://graph.nhaccuatui.com/v1/songs/'+id+'?access_token='+token
    req = requests.get(linklist)
    data = json.loads(req.text)
    if 'data' in data:
        return data['data']

@app.route("/")
def index():  
    return render_template('index.html')

@app.route("/get.html" , methods=['POST'])
def getNctP():  
    link = request.form['url']
    songId = getID(link)
    if songId != None:
        token = createToken()
        songData = songJson(songId,token)
        return render_template('result.html', songData=songData)
    else:
        return "Ahuhu"

@app.route("/api.html")
def getNctAPI():  
    url = request.args.get('url')
    if url == None:
        messages = [{ "text": "URL bạn nhập có vẻ không hợp lệ!" }]
        return jsonify({'messages': messages})
    else:
        songId = getID(url)
        if songId != None:
            token = createToken()
            songData = songJson(songId,token)
            messages = [{ "text": "Tên Bài Hát:" + songData[str(2)].encode('utf-8') + " - " + songData[str(3)].encode('utf-8') + "\n" + "Link 128:" + songData[str(11)].encode('utf-8')}]
            return jsonify({'messages': messages})  


if __name__ == "__main__":  
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)