from settings import *

anime = AnimeDataGetter()
url = 'http://anime.kankan.com/'
reqData = anime.getURL(url)
animeList = []
updateList = re.compile(r'updateList_week_data\[[\d]+\] = \{(.*)\}')
for updateItem in updateList.findall(reqData):
    updateJson = json.loads('{'+updateItem+'}')
    animeList.append({
        "week": updateJson["day_id"],
        "time": updateJson["schedule"].split(' ')[1],
        "url": updateJson["link"],
        "name": updateJson["title"],
    })

db.update('schedule', where='id=1', raw_data=json.dumps(animeList))

req_data = anime.getURL(url)
anime_list = []

update_list = re.compile(r'<li>\d\d:\d\d.*<a.*')
update_time = re.compile(r'<ul id="sche_show_\d">')
time = re.compile(r'\d\d:\d\d')
href = re.compile(r'http://.*\d\d\d\d\d')
name = re.compile(r'">.*</a>')
for i in req_data.split('\n'):
    if update_time.findall(i):
        weekday = update_time.findall(i)[0].split('"')[1].split('_')[2]
        data = update_list.findall(i)[0].decode('utf8')
        anime_list.append({
            "week": weekday,
            "time": time.findall(data)[0],
            "url": href.findall(data)[0],
            "name": name.findall(data)[0].strip('">').split('<')[0]
        })

db.update('schedule', where='id=2', raw_data=json.dumps(animeList))