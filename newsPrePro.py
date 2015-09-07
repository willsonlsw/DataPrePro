#coding=utf-8
import sys
import jieba
import math

reload(sys)
sys.setdefaultencoding('utf-8')

def loadStopWords():
	f = open('stopWords.txt', 'r')
	lines = f.readlines()
	stop_words = set()
	for line in lines:
		stop_words.add(line.split('\n')[0])
	stop_words.add('\r')
	stop_words.add('\n')
	stop_words.add('\r\n')
	stop_words.add('')	
	return stop_words

def calNewsFeature(path):
	f = open(path)
	line = f.readline()
	lines = f.readlines()
	all_news = {}

	stop_words = loadStopWords()

	title_w_df = {}
	content_w_df = {}

	count = 0
	for line in lines:
		count += 1
		if count % 100 == 0:
			print count
			#if count >= 300:
			#	break 

		arrs = line.split('\t')
		if len(arrs) < 7:
			continue

		attrs = arrs[0].split(':')
		url = attrs[1] + ':' + attrs[2]
		
		news = {}
		title = arrs[1].split(':')[1]
		news['publish_time'] = arrs[2].split(':')[1]
		news['source'] = arrs[3].split(':')[1]
		news['score'] = arrs[5].split(':')[1]
		content = arrs[6].split(':')[1]

		title_tmp = list(jieba.cut(title, cut_all = True))
		title_list = []
		for w in title_tmp:
			if not str(w) in stop_words:
				title_list.append(w)
		title_dict = {}
		for w in title_list:
			if not w in title_dict:
				title_dict[w] = 1
			else:
				title_dict[w] += 1
		for w in title_dict:
			if not w in title_w_df:
				title_w_df[w] = 1
			else:
				title_w_df[w] += 1
		
		content_tmp = list(jieba.cut(content))
		content_list = []
		for w in content_tmp:
			if not str(w) in stop_words:
				content_list.append(w)
		content_dict = {}
		for w in content_list:
			if not w in content_dict:
				content_dict[w] = 1
			else:
				content_dict[w] += 1
		for w in content_dict:
			if not w in content_w_df:
				content_w_df[w] = 1
			else:
				content_w_df[w] += 1

		news['title'] = title_dict
		news['content'] = content_dict
		
		all_news[url] = news
	
	print 'title diff words:%d'%len(title_w_df)
	count = 0
	for w in title_w_df:
		if title_w_df[w] > 1:
			count += 1
	print 'word count > 1 %d'%count
	print 'content diff words:%d'%len(content_w_df)
	toune = 0
	for w in content_w_df:
		if content_w_df[w] > 1:
			count += 1
	print 'word count > 1 %d'%count
		
	newsN = len(all_news)
	for i in all_news:
		for w in all_news[i]['title']:
			all_news[i]['title'][w] = all_news[i]['title'][w] * math.log(newsN / title_w_df[w]) / 10.0	
		for w in all_news[i]['content']:
			all_news[i]['content'][w] = all_news[i]['content'][w] * math.log(newsN / content_w_df[w]) / 10.0
			
	return all_news, title_w_df, content_w_df


def output(news, path):
	f = open(path, 'w')
	for url in news:
		f.write('%s\t'%url)
		f.write('%s\t'%news[url]['score'])
		f.write('%s\t'%news[url]['source'])
		f.write('%s\t'%news[url]['publish_time'])
		
		f.write('title:')	
		for w in news[url]['title']:
			f.write('%s:%.4f,'%(w, news[url]['title'][w]))

		f.write('\t')
		f.write('content:')
		for w in news[url]['content']:
			f.write('%s:%.4f,'%(w, news[url]['content'][w]))

		f.write('\n')
	
	f.close()


def newsFeatureVector(newsInfo_path):
	all_news, title_w_df, content_w_df = calNewsFeature(newsInfo_path)

	newsindex = {}
	newsN = 0
	for news in all_news:
		if not news in newsindex:
			newsN += 1
			newsindex[news] = newsN

	title_w_index = {}
	title_wN = 0
	for w in title_w_df:
		if title_w_df[w] >= 1:
			title_wN += 1
			title_w_index[w] = title_wN
	
	content_w_index = {}
	content_wN = 0
	for w in content_w_df:
		if content_w_df[w] >= 2:
			content_wN += 1
			content_w_index[w] = content_wN

	newsfeatures = {}
	for nid in all_news:
		featureV = []
		
		featureV.append(str(newsindex[nid]) + ':1')
		featureV.append(str(newsN + 1) + ':' + all_news[nid]['score'])

		for w in all_news[nid]['title']:
			if w in title_w_index:
				featureV.append(str(newsN + 1 + title_w_index[w]) + ':' + '%.3f'%all_news[nid]['title'][w])

		for w in all_news[nid]['content']:
			if w in content_w_index:
				featureV.append(str(newsN + 1 + title_wN + content_w_index[w]) + ':' + '%.3f'%all_news[nid]['content'][w])
		
		newsfeatures[nid] = featureV
	
	return newsfeatures



if __name__ == '__main__':
	newsInfo_path = '../naviNewsData/newsInfo.txt'
	feature_out_path = 'data/newsFeatureInfo.txt'

	#jieba.enable_parallel(2)

	#news, title_w_df, content_w_df = calNewsFeature(newsInfo_path)
	#output(news, feature_out_path)
	nfvs = newsFeatureVector(newsInfo_path)
	f = open('data/newsFeatureVectors.txt','w')
	for nid in nfvs:
		f.write('%s '%nid)
		for fea in nfvs[nid]:
			f.write('%s '%fea)
		f.write('\n')
	f.close()
