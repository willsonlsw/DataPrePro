#coding=utf-8
import os
import sys
import time

reload(sys)
sys.setdefaultencoding('utf-8')

def loadNewsInfo(path):
	f = open(path, 'r')
	line = f.readline()
	lines = f.readlines()
	f.close()
	all_news = {}
	for line in lines:
		arrs = line.split('\t')
		if len(arrs) < 7:
			continue
		urlattr = arrs[0].split(':')
		news = {}
		for i in range(1, len(arrs)):
			if i == 4 or i == 6: 
				continue
			attrs = arrs[i].split(':')
			#if urlattr[1] + ':' + urlattr[2] == 'http://ent.163.com/15/0812/01/B0PFMQIP00031H2L.html':
			#	print attrs
			if len(attrs) >= 2:
				news[attrs[0]] = attrs[1]
				for j in range(2, len(attrs)):
					news[attrs[0]] += ':' + attrs[j]
			else:
				news[attrs[0]] = ''
			#print news
		all_news[urlattr[1] + ':' + urlattr[2]] = news
		#print urlattr[1] + urlattr[2]
	return all_news


def loadShowAndClickInfo(path):
	f = open(path, 'r')
	line = f.readline()
	line = f.readline()
	lines = f.readlines()
	f.close()
	user_clicks = {}
	showlists = []
	for line in lines:
		arrs = line.split('\r')[0].split('\t')
		userID = arrs[0]
		if arrs[1] == 'getcontent':
			if not arrs[3] == '头条推荐':
				continue

			if not userID in user_clicks:
				user_clicks[userID] = []
			click = {}
			click['type'] = arrs[2]
			click['channel'] = arrs[3]
			click['url'] = arrs[4]
			click['time_stamp'] = arrs[5].split('\r')[0]
			user_clicks[userID].append(click)
		elif arrs[1] == 'showlist':
			if not userID in showlists:
				showlists[userID] = []
			if len(showlists[userID]) == 0 or (not showlists[userID][len(showlists[userID]) - 1]['urls'] == arrs[3]):
				showlist = {}
				showlist['type'] = arrs[2]
				showlist['urls'] = arrs[3]
				showlist['time_stamp'] = arrs[4]
				showlists[userID].append(showlist)
				
	return user_clicks, showlists


def userClickNews(news, users_clicks, showlists, path):
	print len(news), len(users_clicks)
	f = open(path, 'w')
	for user in users_clicks:
		f.write('%s------------------------------------------\n'%user)
		clicks = users_clicks[user]
		for click in clicks:
			#print click['url']
			if click['url'] in news:
				#print click['url'],news[click['url']]
				f.write('title:%s\t'%news[click['url']]['title'])
				f.write('score:%s\t'%news[click['url']]['score'])
				f.write('channel:%s\t'%click['channel'])
				f.write('time_stamp:%s\n'%click['time_stamp'].split('\r')[0])
		f.write('--------------------------------------------------------------\n')
		f.write('--------------------------------------------------------------\n')
	f.write('################################################################\n')
	
	count = 0
	for item in showlists:
		count += 1
		f.write('%d\t%s\t%s\n'%(count, item['urls'], item['time_stamp']))

	f.close()


if __name__ == '__main__':
	sc_file_path = '../naviNewsData/showAndClickInfo.txt'
	news_info_path = '../naviNewsData/newsInfo.txt'
	user_click_news_path = 'data/userClickNews.txt'

	news = loadNewsInfo(news_info_path)
	users_clicks, showlists = loadShowAndClickInfo(sc_file_path)
	#userClickNews(news, users_clicks, showlists, user_click_news_path)
