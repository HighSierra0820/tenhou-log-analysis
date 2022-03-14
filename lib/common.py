from mahjong import shanten as st

pai1 = [
	'1m', '1m', '1m', '1m', '2m', '2m', '2m', '2m', '3m', '3m', '3m', '3m',
	'4m', '4m', '4m', '4m', '0m', '5m', '5m', '5m', '6m', '6m', '6m', '6m',
	'7m', '7m', '7m', '7m', '8m', '8m', '8m', '8m', '9m', '9m', '9m', '9m',
	'1p', '1p', '1p', '1p', '2p', '2p', '2p', '2p', '3p', '3p', '3p', '3p',
	'4p', '4p', '4p', '4p', '0p', '5p', '5p', '5p', '6p', '6p', '6p', '6p',
	'7p', '7p', '7p', '7p', '8p', '8p', '8p', '8p', '9p', '9p', '9p', '9p',
	'1s', '1s', '1s', '1s', '2s', '2s', '2s', '2s', '3s', '3s', '3s', '3s',
	'4s', '4s', '4s', '4s', '0s', '5s', '5s', '5s', '6s', '6s', '6s', '6s',
	'7s', '7s', '7s', '7s', '8s', '8s', '8s', '8s', '9s', '9s', '9s', '9s',
	'東', '東', '東', '東', '南', '南', '南', '南', '西', '西', '西', '西', '北', '北', '北', '北',
	'白', '白', '白', '白', '發', '發', '發', '發', '中', '中', '中', '中',
]

pai2 = [
	'1m', '1m', '1m', '1m', '2m', '2m', '2m', '2m', '3m', '3m', '3m', '3m',
	'4m', '4m', '4m', '4m', '5m', '5m', '5m', '5m', '6m', '6m', '6m', '6m',
	'7m', '7m', '7m', '7m', '8m', '8m', '8m', '8m', '9m', '9m', '9m', '9m',
	'1p', '1p', '1p', '1p', '2p', '2p', '2p', '2p', '3p', '3p', '3p', '3p',
	'4p', '4p', '4p', '4p', '5p', '5p', '5p', '5p', '6p', '6p', '6p', '6p',
	'7p', '7p', '7p', '7p', '8p', '8p', '8p', '8p', '9p', '9p', '9p', '9p',
	'1s', '1s', '1s', '1s', '2s', '2s', '2s', '2s', '3s', '3s', '3s', '3s',
	'4s', '4s', '4s', '4s', '5s', '5s', '5s', '5s', '6s', '6s', '6s', '6s',
	'7s', '7s', '7s', '7s', '8s', '8s', '8s', '8s', '9s', '9s', '9s', '9s',
	'1z', '1z', '1z', '1z', '2z', '2z', '2z', '2z', '3z', '3z', '3z', '3z', '4z', '4z', '4z', '4z',
	'5z', '5z', '5z', '5z', '6z', '6z', '6z', '6z', '7z', '7z', '7z', '7z',
]

yaku = [
	# 一飜
	'門前清自摸和','立直','一発','槍槓','嶺上開花',
	'海底摸月','河底撈魚','平和','断幺九','一盃口',
	'自風 東','自風 南','自風 西','自風 北',
	'場風 東','場風 南','場風 西','場風 北',
	'役牌 白','役牌 發','役牌 中',
	# 二飜
	'両立直','七対子','混全帯幺九','一気通貫','三色同順',
	'三色同刻','三槓子','対々和','三暗刻','小三元','混老頭',
	# 三飜
	'二盃口','純全帯幺九','混一色',
	# 六飜
	'清一色',
	# 満貫
	'人和',
	# 役満
	'天和','地和','大三元','四暗刻','四暗刻単騎','字一色',
	'緑一色','清老頭','九蓮宝燈','純正九蓮宝燈','国士無双',
	'国士無双13面','大四喜','小四喜','四槓子',
	# 懸賞役
	'ドラ','裏ドラ','赤ドラ'
]

ten_class = [
	'', '満貫', '跳満', '倍満', '三倍満', '役満'
]

ryuukyoku_type = {
	'yao9': '九種九牌',
	'reach4': '四家立直',
	'ron3': '三家和了',
	'kan4': '四槓散了',
	'kaze4': '四風連打',
	'nm': '流し満貫',
}

def printtehai(arr):
	if len(arr)!=136 and len(arr)!=34:
		return
	if len(arr)==136:
		str=""
		for i in range(0,136):
			if arr[i]==1:
				str=str+pai2[i]
		return str
	if len(arr)==34:
		str=""
		for i in range(0,34):
			if arr[i]==1:
				str=str+pai2[i*4]
		return str

def dfs(tehai,cnt):
#	print(tehai,end=' ')
#	print(cnt)
	if cnt==0:
		return 1
	for i in range(0,34):
		if tehai[i]==0:
			continue
		if tehai[i]>=3:
			tehai[i]=tehai[i]-3
			if dfs(tehai,cnt-3):
				return 1
			tehai[i]=tehai[i]+3
		if i<27 and i%9<7 and tehai[i]>=1 and tehai[i+1]>=1 and tehai[i+2]>=1:
			tehai[i]=tehai[i]-1
			tehai[i+1]=tehai[i+1]-1
			tehai[i+2]=tehai[i+2]-1
			if dfs(tehai,cnt-3):
				return 1
			tehai[i]=tehai[i]+1
			tehai[i+1]=tehai[i+1]+1
			tehai[i+2]=tehai[i+2]+1
		if tehai[i]!=0:
			return 0

def convstr(hai):
	if type(hai)==int:
		return pai2[hai]
	if type(hai)==list:
		str=""
		for i in hai:
			str=str+pai2[i]
		return str

routoupai=[0,8,9,17,18,26,27,28,29,30,31,32,33]

def calctempai(pai136):
	if len(pai136)!=136:
		return []
	if pai136.count(1)%3!=1:
		return []
	total=pai136.count(1)
	ret=[0 for i in range(34)]
	pai34=[0 for i in range(34)]
	for i in range(136):
		pai34[i//4]=pai34[i//4]+pai136[i]
	cnt=[0 for i in range(4)]
	cntmod3=[0 for i in range(4)]
	for i in range(34):
		cnt[i//9]=(cnt[i//9]+pai34[i])
	for i in range(4):
		cntmod3[i]=cnt[i]%3
	assert((pai34.count(2)==6 and pai34.count(1)==1) or \
		(pai34.count(1)>=11 and sum(pai34[i] for i in routoupai)==13) or\
		((cntmod3.count(2)==2 and cntmod3.count(0)==2)or(cntmod3.count(1)==1 and cntmod3.count(0)==3)))
	if pai34.count(2)==6 and pai34.count(1)==1:
		ret[pai34.index(1)]=1
	if pai34.count(1)>=11 and sum(pai34[i] for i in routoupai)==13:
		if pai34.count(1)==11:
			for i in routoupai:
				if pai34[i]==0:
					ret[i]=1
					break
		else:
			for i in routoupai:
				ret[i]=1
	for i in range(0,34):#ver 2
		pai34plus=[pai34[i] for i in range(0,34)]
		pai34plus[i]=pai34plus[i]+1
		for j in range(0,34):
			if pai34plus[j]>=2:
				pai34plus[j]=pai34plus[j]-2
				if dfs(pai34plus,total+1-2):
					ret[i]=1
					break
				pai34plus[j]=pai34plus[j]+2
# 	if cntmod3.count(1)==1 and cntmod3.count(0)==3: #ver 1
# 		color=cntmod3.index(1)*9
# 		if color==27:
# 			for i in range(27,34):
# 				if pai34[i]==1:
# 					ret[i]=1
# 					return ret
# 		for i in range(color,color+9):
# 			if(pai34[i]==4):
# 				continue
# 			pai34plus=[pai34[j] for j in range(0,34)]
# 			pai34plus[i]=pai34plus[i]+1
# 			for j in range(color,color+9):
# #				print(i,j)
# 				if pai34plus[j]>=2:
# 					pai34plus[j]=pai34plus[j]-2
# 					if dfs(pai34plus,color,cnt[color//9]-1):
# 						ret[i]=1
# 						break
# 					pai34plus[j]=pai34plus[j]+2
# 	if cntmod3.count(2)==2 and cntmod3.count(0)==2:
# 		colors=[]
# 		for i in range(0,4):
# 			if cntmod3[i]==2:
# 				colors.append(i*9)
# 		color1=colors[0]
# 		color2=colors[1]
# 		limit1=9
# 		limit2=9
# 		if color1==27:
# 			limit1=limit1-2
# 		if color2==27:
# 			limit2=limit2-2
# 		for i in range(color1,color1+limit1):
# 			if(pai34[i]==4):
# 				continue
# 			pai34plus=[pai34[j] for j in range(0,34)]
# 			pai34plus[i]=pai34plus[i]+1
# 			for j in range(color2,color2+limit2):
# 				if pai34plus[j]>=2:
# 					pai34plus[j]=pai34plus[j]-2
# 					if dfs(pai34plus,color1,cnt[color1//9]+1) and dfs(pai34plus,color2,cnt[color2//9]-2):
# 						ret[i]=1
# 						break
# 					pai34plus[j]=pai34plus[j]+2
# 		for i in range(color2,color2+limit2):
# 			if(pai34[i]==4):
# 				continue
# 			pai34plus=[pai34[j] for j in range(0,34)]
# 			pai34plus[i]=pai34plus[i]+1
# 			for j in range(color1,color1+limit1):
# 				if pai34plus[j]>=2:
# 					pai34plus[j]=pai34plus[j]-2
# 					if dfs(pai34plus,color2,cnt[color2//9]+1) and dfs(pai34plus,color1,cnt[color1//9]-2):
# 						ret[i]=1
# 						break
# 					pai34plus[j]=pai34plus[j]+2
	return ret

# kokushi 13 men machi
# [1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 1,0,0,0,
#  1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 1,0,0,0,
#  1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 1,0,0,0,
#  1,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0]

# chiitoi
# [1,0,1,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 1,0,0,1,
#  1,0,1,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 1,0,0,1,
#  1,0,1,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 1,0,0,0,
#  1,0,1,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0]

# ippankei
# [1,1,1,0, 1,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0, 1,1,1,0,
#  0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0,
#  0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0,
#  0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0]

# ippankei
# [0,0,0,0, 0,0,0,0, 0,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0, 1,1,1,0,
#  1,1,1,0, 1,0,0,0, 1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0,
#  0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0,
#  0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0]
