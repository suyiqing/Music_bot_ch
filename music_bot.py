#coding=utf-8

from flask import Flask, request, jsonify 
import json
import requests

app = Flask(__name__)
port = '5000'

@app.route('/genre', methods=['POST']) 
def get_by_category(): 

  bot_data = json.loads(request.get_data())
  headers = {
    "Authorization": "Bearer BQBw4S5EJVFOzNpB7rV45Ej8uV0xKO7NG727gH-lNUSMqruwtwBgiCU7HWrT5cS8Yfp52ejJQqZdJplqW-DotB11LYdGXvbF4L9kOj5S6ksgIR1ZD832sgPFTbEJTEa3n3rH4peqz-9Iw4LmoQ8i-kPvxcTBzIKUUw"
    }
  category_id = bot_data['conversation']['memory']['genre']['id']

  url = "https://api.spotify.com/v1/browse/categories/" + category_id + "/playlists?limit=10"
  r = requests.get(url, headers=headers)
  data = r.json()
  items = data['playlists']['items']
  playlists = []

  for item in items:
    playlist = {
      "title": "歌单：",
      "subtitle": item["name"],
      "imageUrl": item["images"][0]["url"],
      "buttons": [
      {
        "title": "开始听",
        "type": "web_url",
        "value": item["external_urls"]["spotify"]
      }]
    }
    playlists.append(playlist)
  
  return jsonify( 
    status=200, 
    replies=[{ 
      'type': 'carousel', 
      'content': playlists,
    }]
  )

@app.route('/artist', methods=['POST']) 
def get_by_artist(): 
  
  bot_data = json.loads(request.get_data())
  headers = {
    "Authorization": "Bearer BQBw4S5EJVFOzNpB7rV45Ej8uV0xKO7NG727gH-lNUSMqruwtwBgiCU7HWrT5cS8Yfp52ejJQqZdJplqW-DotB11LYdGXvbF4L9kOj5S6ksgIR1ZD832sgPFTbEJTEa3n3rH4peqz-9Iw4LmoQ8i-kPvxcTBzIKUUw"
    }

  artist_value = bot_data['conversation']['memory']['artist']['value']

  if ' ' in artist_value:
    artist_value.replace(' ', '%20')

  url = "https://api.spotify.com/v1/search?q=" + artist_value + "&type=track&limit=10"
  r = requests.get(url, headers=headers)
  data = r.json()

  if not data['tracks']['items']:
    return jsonify( 
      status=200, 
      replies=[{ 
        'type': 'text', 
        'content': '对不起，我不能找到这个歌手', 
      },
      { 
        'type': 'text', 
        'content': '你可以试试别的歌手', 
      }]
    )

  items = data['tracks']['items']

  songs = []

  for item in items:
    song = {
      "title": "歌名：",
      "subtitle": item["name"],
      "imageUrl": item['album']["images"][0]["url"],
      "buttons": [{
        "title": "开始听",
        "type": "web_url",
        "value": item["external_urls"]["spotify"]
      }]
    }
    songs.append(song)

  return jsonify( 
    status=200, 
    replies=[
    {
      'type': 'text', 
      'content': '好的，这是我找到的歌 🥳',
    },
    { 
      'type': 'carousel', 
      'content': songs, 
    }]
  ) 
 
@app.route('/errors', methods=['POST']) 
def errors(): 
  print(json.loads(request.get_data())) 
  return jsonify(status=200) 
 
app.run(port=port)
