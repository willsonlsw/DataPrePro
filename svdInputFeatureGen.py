#coding=utf-8
import os
import sys
import random
from userPrePro import userFeatureVector
from newsPrePro import newsFeatureVector
from userNewsRating import userNewsRating

reload(sys)
sys.setdefaultencoding('utf-8')


def featuresFileGen(train_path, test_path, usersVectors, newsVectors, ratings):
	ftrain = open(train_path, 'w')
	ftest = open(test_path, 'w')
	
	for uid in ratings:
		for url in ratings[uid]:
			if not url in newsVectors:
				continue

			x = random.uniform(0, 1)
			if x < 0.8:
				ftrain.write('%d '%ratings[uid][url])
				ftrain.write('0 ')
				ftrain.write('%d '%len(usersVectors[uid]))
				ftrain.write('%d '%len(newsVectors[url]))
				for uf in usersVectors[uid]:
					ftrain.write('%s '%uf)
				for nf in newsVectors[url]:
					ftrain.write('%s '%nf)
				ftrain.write('\n')
			
			else:
				ftest.write('%d '%ratings[uid][url])
				ftest.write('0 ')
				ftest.write('%d '%len(usersVectors[uid]))
				ftest.write('%d '%len(newsVectors[url]))
				for uf in usersVectors[uid]:
					ftest.write('%s '%uf)
				for nf in newsVectors[url]:
					ftest.write('%s '%nf)
				ftest.write('\n')

	ftest.close()
	ftrain.close()


if __name__ == '__main__':
	userInfo_path = '../naviNewsData/userInfo.txt'
	newsInfo_path = '../naviNewsData/newsInfo.txt'
	sc_path = '../naviNewsData/showAndClickInfo.txt'

	train_data_path = 'data/trainData.txt'
	test_data_path = 'data/testData.txt'

	usersVectors = userFeatureVector(userInfo_path)
	newsVectors = newsFeatureVector(newsInfo_path)
	ratings = userNewsRating(sc_path)
	
	featuresFileGen(train_data_path, test_data_path, usersVectors, newsVectors, ratings)
