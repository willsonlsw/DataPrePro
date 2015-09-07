#coding=utf-8
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def loadShowAndClickInfo(path):
	f = open(path, 'r')
	line = f.readline()
	line = f.readline()
	lines = f.readlines()
	f.close()
	user_clicks = {}
	showlists = {}
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
			#if len(showlists[userID]) == 0 or (not showlists[userID][len(showlists[userID]) - 1]['urls'] == arrs[3]):
			showlist = {}
			showlist['type'] = arrs[2]
			showlist['urls'] = arrs[3].split(' ')
			showlist['time_stamp'] = arrs[4]
			showlists[userID].append(showlist)
				
	return user_clicks, showlists

def userNewsRating(path):
	user_clicks, showlists = loadShowAndClickInfo(path)
	
	users_ratings = {}

	for uid in user_clicks:
		ratings = {}
		listcount = 0
		for clk in user_clicks[uid]:
			url = clk['url']
			while listcount < len(showlists[uid]) and showlists[uid][listcount]['time_stamp'] <= clk['time_stamp']:
				listcount += 1
			
			if listcount == len(showlists[uid]):
				listcount -= 1
			#print len(showlists[uid]), listcount		
			k = listcount
			while k > 0 and not(url in showlists[uid][k]['urls']):
				k -= 1
			
			#print uid, listcount, k,
			
			urlindex = 0
			while urlindex < 12 and (not url == showlists[uid][k]['urls'][urlindex]):
				urlindex += 1

			#print urlindex

			if urlindex < 12:
				ratings[url] = 1

				near_index = [-4, -2, 2, 4]
				for j in near_index:
					if urlindex + j >= 0 and urlindex + j< 12:
						if not showlists[uid][k]['urls'][urlindex + j] in ratings:
							ratings[showlists[uid][k]['urls'][urlindex + j]] = 0
		users_ratings[uid] = ratings

	return users_ratings
							

if __name__ == '__main__':
	sc_path = '../naviNewsData/showAndClickInfo.txt'

	ratings = userNewsRating(sc_path)
	f = open('data/ratings.txt', 'w')
	for uid in ratings:
		f.write('%s '%uid)
		r1 = 0
		r0 = 0
		for url in ratings[uid]:
			if ratings[uid][url] == 1:
				r1 += 1
			if ratings[uid][url] == 0:
				r0 += 1
		f.write('%d %d '%(r1, r0))
		for url in ratings[uid]:
			f.write('%s:%d '%(url, ratings[uid][url]))
		f.write('\n')
	f.close()
