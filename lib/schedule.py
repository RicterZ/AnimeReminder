import re, json
from anime import AnimeDataGetter

anime = AnimeDataGetter()
url = 'http://anime.kankan.com/'
req_data = anime.getURL(url)

anime_list = []
updateList = re.compile('updatelist_week_data\[\d+\] = \{(.*)\};')
for updateItem in updateList.findall(req_data):
    updateJson = json.loads('{'+updateItem+'}')
    anime_list.append({
        "week": updateJson["day_id"],
        "time": updateJson["schedule"].split(' ')[1],
        "url": updateJson["link"],
        "name": updateJson["title"],
    })
db.update('schedule', where='id=1', raw_data=json.dumps(anime_list))

anime_list = []
update_list = re.compile('<ul id="sche_show_(\d)">([\w\W]+?)</ul>')
update_data = re.compile('<li>(\d{2}\:\d{2}).*<a  href="(.*)" blockid="\d\d\d\d">(.*)</a></li>')
for i in update_list.findall(req_data):
    for data in update_data.findall(i[1]):
        anime_list.append({
            "week": i[0],
            "time": data[0],
            "url": data[1],
            "name": data[2],
        })
db.update('schedule', where='id=2', raw_data=json.dumps(anime_list))