import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def mergeLabel(inpath):
	f = open(inpath, 'r')
	line = f.readline()
	lines = f.readlines()
	f.close()

	#fout = open(outpath, 'w')

	labelset = set()
	all_users = {}
	for line in lines:
		arrs = line.split('\r')[0].split('\t')
		userID = arrs[0]
		position = arrs[1]
		sex = arrs[2]
		interests = {}
		users = {}
		for i in range(3, len(arrs)):
			label, score = arrs[i].split(':')
			if '.' in label:
				label = label.split('.')[0]
			if label in interests:
				interests[label].append(score)
			else:
				interests[label] = [score]
		
			if not label in labelset:
				labelset.add(label)
		#print userID, interests
		
		#fout.write('%s\t'%userID)
		#fout.write('%s\t'%position)
		#fout.write('%s\t'%sex)
		tmp = {}
		for ist in interests:
			ssum = 0.0
			for x in interests[ist]:
				ssum += float(x)
			#print ist,interests[ist]
			tmp[ist] = ssum / len(interests[ist])
			#fout.write('%s:%.3f\t'%(ist, tmp[ist]))
		#fout.write('\n')
	
		users['position'] = position
		users['sex'] = sex
		users['interests'] = tmp
		all_users[userID] = users
	
	#fout.write('labels\t')
	#for label in labelset:
		#fout.write('%s\t'%label)
	
	#fout.close()

	return all_users, labelset


def userFeatureVector(userInfo_path):
	all_users, labelset = mergeLabel(userInfo_path)
	labelindex = {}
	labelcount = 1
	for label in labelset:
		if not label in labelindex:
			labelindex[label] = labelcount
			labelcount += 1
	usersfeatures = {}

	uidcount = 1
	userN = len(all_users)
	for uid in all_users:
		features = []

		features.append(str(uidcount) + ':' + '1')
		uidcount += 1
		
		for ist in all_users[uid]['interests']:
			istlabelind = labelindex[ist]
			features.append(str(userN + istlabelind) + ':' + '%.3f'%all_users[uid]['interests'][ist])
		
		usersfeatures[uid] = features
		#print uid, features

	return usersfeatures


if __name__ == "__main__":
	userInfo_path = '../naviNewsData/userInfo.txt'
	userInfo_out_path = 'data/userInfo_pre.txt'

	all_users, labelset = mergeLabel(userInfo_path)
	ufvs = userFeatureVector(userInfo_path)
	f = open('data/userFeatureVectors.txt', 'w')
	for uid in ufvs:
		f.write('%s '%uid)
		for ist in ufvs[uid]:
			f.write('%s '%ist)
		f.write('\n')
	f.close()


