import re
from lib import xmlparser as xp
from lib import common as cm
import sys

result={
	"總局數":0,
	"和牌次數":0,
	"立直數":0,
	"先制":0,
	"追立":0,
#	"先制兩面":0,
#	"追立兩面":0,
	"14自摸4":0,
	"14自摸1":0,
	"14榮和4":0,
	"14榮和1":0,
}

# print("Tenhou paifu analyser by SomeyaMako")
debug=0
args=sys.argv
if len(args)<2:
	exit()
if args[1]=='-d':
	args=args[2:]
	debug=1
else:
	args=args[1:]
for paifuname in args:
	xp.ans=[]
	arr=xp.parse(paifuname)
	oya=0
	tehai=[[0 for i in range(136)] for j in range(4)]
	fuuro=[[],[],[],[]]
	# fuuro format:
	# [type,pai136,attrdict]
	# chii: "chii", tiles[], base, whichoutof3
	# pon: "pon", tiles[], base, whichoutof3, fromwho
	# shouminkan: "shouminkan", tiles[], base, whichoutof3, fromwho
	# daiminkan: "daiminkan", tiles[], base, whichoutof4, fromwho
	# ankan: "ankan", tiles[], base, whichoutof4
	kyoku=0
	homba=0
	kyoutaku=0
	doralist=[]
	riichi=[]
	for data in arr:
		if data[0]=='mjloggm' or data[0]=='SHUFFLE'\
		or data[0]=='GO' or data[0]=='UN'\
		or data[0]=='BYE' or data[0]=='TAIKYOKU':
			continue
		if data[0]=='INIT':

			result['總局數']=result['總局數']+1
			anyone_riichi=0
			who_sensei=0
			isriichi=[0,0,0,0]

			tehai=[[0 for i in range(136)] for j in range(4)]
			fuuro=[[],[],[],[]]
			attrdict=data[1]
			seedarr=attrdict['seed'].split(',')
			kyoku=int(seedarr[0])
			homba=int(seedarr[1])
			kyoutaku=int(seedarr[2])
			doralist=[int(seedarr[5])]
			oya=int(attrdict['oya'])
			for i in range(0,4):
				tehailist=attrdict['hai'+str(i)].split(',')
				for j in tehailist:
					tehai[i][int(j)]=1
	#		if debug:
	#			print('kyoku:'+str(kyoku)+', homba:'+str(homba), end='\t')
	#			for i in range(0,4):
	#				print(cm.printtehai(tehai[i]))
	#			print("")
		elif data[0]=='DORA':
		# shin dora
			dorahai=int(data[1]['hai'])
			doralist.append(dorahai)
		elif data[0]=='N':
			who=int(data[1]['who'])
			typeraw=data[1]['m']
			typestr=format(int(typeraw), '#018b')[2:]
			if typestr[13] == '1': # chii
				chiipai=int(typestr[0:6],2)
				called=chiipai%3
				base=(chiipai-called)//3
				base=base+(base//7)*2
				t=[0,0,0]
				for i in range(0,3):
					tiraw=int(typestr[11-2*i:13-2*i],2)
					t[i]=tiraw+base*4+4*i
	#				if debug:
	#					print(cm.pai2[t[i]],end='')
				for i in range(0,3):
					if i!=called:
						assert(tehai[who][t[i]]==1)
						tehai[who][t[i]]=0
				fuuro[who].append(["chii",t,base,called])
	#			if debug:
	#				print(fuuro[who][-1])
			else:
				if typestr[12] == '1': # pon
					fromwho=int(typestr[14:],2)
					ponpai=int(typestr[0:7],2)
					base=ponpai//3
					called=ponpai%3
					t=[]
					t4raw=int(typestr[9:11],2)
					for i in range(base*4,base*4+4):
						if t4raw+base*4!=i:
							t.append(i)
					for i in range(0,3):
						if i!=called:
							assert(tehai[who][t[i]]==1)
							tehai[who][t[i]]=0
	#					if debug:
	#						print(cm.pai2[t[i]],end='')
					fuuro[who].append(["pon",t,base,called,fromwho])
	#				if debug:
	#					print(fuuro[who][-1])
				if typestr[11] == '1': # shouminkan
					kakampai=int(typestr[0:7],2)
					base=kakampai//3
					t4raw=int(typestr[9:11],2)
					totalfuuro=len(fuuro[who])
					assert(tehai[who][t4raw+base*4]==1)
					tehai[who][t4raw+base*4]=0
					for i in range(totalfuuro):
						if base==fuuro[who][i][2]:
							fuuro[who][i][0]="shouminkan"
			if typestr[11:14] == '000': # ankan aruiwa daiminkan
				if typestr[14:] == '00': # ankan
					ankampai=int(typestr[0:8],2)
					base=ankampai//4
					called=ankampai%4
					t=[]
					for i in range(0,4):
						assert(tehai[who][base*4+i]==1)
						tehai[who][base*4+i]=0
						t.append(base*4+i)
	#					if debug:
	#						print(cm.pai2[t[i]],end='')
					fuuro[who].append(["ankan",t,base,called])
	#				if debug:
	#					print(fuuro[who][-1])
				else: # daiminkan
					daiminkampai=int(typestr[0:8],2)
					base=daiminkampai//4
					called=daiminkampai%4
					fromwho=int(typestr[14:],2)
					t=[]
					for i in range(0,4):
						if i!=called:
							assert(tehai[who][base*4+i]==1)
							tehai[who][base*4+i]=0
						t.append(base*4+i)
						if debug:
							print(cm.pai2[t[i]],end='')
					fuuro[who].append(["daiminkan",t,base,called,fromwho])
					if debug:
						print(fuuro[who][-1])
		elif data[0]=='RYUUKYOKU':
			pass
		# ryuukyoku
		# paifu with ryuukyoku needed
			if debug:
				print("                        ",end='')
				print("RYUUKYOKU")
		elif data[0]=='REACH':
		# riichi
		# once again, the term riichi and the word reach are unrelevant
			who=int(data[1]['who'])
			step=int(data[1]['step'])

			if step==1:
				result['立直數']=result['立直數']+1
				if anyone_riichi==0:
					result['先制']=result['先制']+1
					anyone_riichi=1
					who_sensei=who
				else:
					result['追立']=result['追立']+1
				
			
			if step==2:
				tempai=cm.calctempai(tehai[who])
				isriichi[who]=1
				print(cm.printtehai(tempai),end='\t')
				print(cm.printtehai(tehai[who]))
#				flag=0
#				for i in range(3):
#					for j in range(6):
#						if tempai[i*9+j]==1 and tempai[i*9+j+3]==1:
#							flag=1
#							break
#					if flag:
#						break
#				if flag:
#					if who_sensei==who:
#						result['先制兩面']=result['先制兩面']+1
#					else:
#						result['追立兩面']=result["追立兩面"]+1
			
	#		if debug and step==2:
	#			print("                        ",end='')
	#			print("RIICHI")
		elif data[0]=='AGARI':
		# agari
		# todo: get tempai-keichou
		# e.g.
		# hht: 1-4 ryammen tempai de riichi shita toki
		#      1 de agatta kaisuu/wariai
		#      6-9 mo onaji
			result['和牌次數']=result['和牌次數']+1
			tenarr=data[1]['ten'].split(',')
			fu=tenarr[0]
			han=0
			ten=int(tenarr[1])
			limit=int(tenarr[2])
			who=int(data[1]['who'])
			fromwho=int(data[1]['fromWho'])
			haistr=data[1]['hai'].split(',')
			agarihai=int(data[1]['machi'])
			
			haiarr=[0 for i in range(136)]
			for i in haistr:
				if int(i)!=agarihai:
					assert(tehai[who][int(i)]==1)
					haiarr[int(i)]=1
			tempaistr=cm.calctempai(haiarr)
			ryammen14flag=0
			if isriichi[who] and tempaistr.count(1)==2:
				for i in range(0,3):
					if (tempaistr[i*9+0]==1 and tempaistr[i*9+3]==1) or\
						(tempaistr[i*9+5]==1 and tempaistr[i*9+8]==1):
	#					result['14立直和出']=result['14立直和出']+1
						if agarihai//4==i*9+0 or agarihai//4==i*9+8:
							if who!=fromwho:
								result["14榮和1"]=result["14榮和1"]+1
							else:
								result["14自摸1"]=result["14自摸1"]+1
						elif agarihai//4==i*9+3 or agarihai//4==i*9+5:
							if who!=fromwho:
								result["14榮和4"]=result["14榮和4"]+1
							else:
								result["14自摸4"]=result["14自摸4"]+1
						else:
							print(cm.printtehai(haiarr),tempaistr,agarihai)
			try:
				yakuraw=data[1]['yaku'].split(',')
			except:
				yakuraw=data[1]['yakuman'].split(',')
			yakuarr=[]
			for i in yakuraw:
				yakuarr.append(int(i))
			yakucount=len(yakuarr)//2
			for i in range(0,yakucount):
				han=han+yakuarr[i*2+1]
			if debug:
				print(str(fromwho)+'->'+str(who),end='')
				print('\t\t',end="")
				print(cm.printtehai(haiarr),end=' ')
				print(cm.convstr(agarihai),end=' ')
	# fuuro format:
	# [type,pai136,attrdict]
	# chii: "chii", tiles[], base, whichoutof3
	# pon: "pon", tiles[], base, whichoutof3, fromwho
	# shouminkan: "shouminkan", tiles[], base, whichoutof3, fromwho
	# daiminkan: "daiminkan", tiles[], base, whichoutof4, fromwho
	# ankan: "ankan", tiles[], base, whichoutof4
				for i in fuuro[who]:
					if i[0]=="chii":
						for j in range(3):
							if i[3]==j:
								print("[",end='')
							print(cm.convstr(i[1][j]),end='')
							if i[3]==j:
								print("]",end='')
						print(' ',end='')
					if i[0]=="pon":
						n=[]
						for j in range(3):
							if j!=i[3]:
								n.append(i[1][j])
						n.insert(3-i[4],i[1][i[3]])
						for j in range(3):
							if 3-i[4]==j:
								print("[",end='')
							print(cm.convstr(n[j]),end='')
							if 3-i[4]==j:
								print("]",end='')
						print(' ',end='')
					if i[0]=="ankan":
						print('#'+cm.convstr(i[1])+'# ')
					if i[0]=="daiminkan":
						n=[]
						for j in range(4):
							if j!=i[3]:
								n.append(i[1][j])
						pos=0
						if i[4]==1:
							n.insert(3,i[1][i[3]])
							pos=3
						if i[4]==2:
							n.insert(1,i[1][i[3]])
							pos=2
						if i[4]==3:
							n.insert(0,i[1][i[3]])
							pos=1
						for j in range(4):
							if j==pos:
								print("[",end='')
							print(cm.convstr(n[j]),end='')
							if j==pos:
								print("]",end='')
						print(' ',end='')
					if i[0]=="shouminkan":
						n=[]
						for j in range(3):
							if j!=i[3]:
								n.append(i[1][j])
						n.insert(3-i[4],i[1][i[3]])
						for j in range(3):
							if 3-i[4]==j:
								print("[",end='')
								for k in range(i[2]*4,i[2]*4+4):
									if k not in i[1]:
										print('('+cm.convstr(k)+')',end='')
							print(cm.convstr(n[j]),end='')
							if 3-i[4]==j:
								print("]",end='')
						print(' ',end='')
				print('')
				for i in range(0,yakucount):
					if yakuarr[i*2+1]!=0:
						print("                           ",end='')
						print(str(yakuarr[i*2+1])+'\t',end="")
						print(cm.yaku[yakuarr[i*2]])
				print("                        ",end='')
				print(str(fu)+'符 '+str(han)+'飜 '+str(ten)+'点 '\
					+cm.ten_class[limit])
		else:
			char=data[0][0]
			pai=int(data[0][1:])
			assert('T'<=char<='W' or 'D'<=char<='G')
			if 'T'<=char<='W':
				who=ord(char)-ord('T')
				assert(tehai[who][pai]==0)
				tehai[who][pai]=1
			if 'D'<=char<='G':
				who=ord(char)-ord('D')
				assert(tehai[who][pai]==1)
				tehai[who][pai]=0
		if debug:
			for i in range(4):
				print('%30s' % cm.printtehai(tehai[i]),end=' ')
			print('')

# print(result, end='\t')
# # print("兩面率 先制 %.3f 追立 %.3f "%(result['先制兩面']/result['先制'],result['追立兩面']/result['追立']), end='')
# print("自摸1 %.3f 榮和1 %.3f"%\
# 	(result['14自摸1']/(result['14自摸1']+result['14自摸4']),\
# 	 result['14榮和1']/(result['14榮和1']+result['14榮和4']))
# 	)

# file1=open("output.txt","a+")
# file1.write(str(result['14自摸1'])+' ')
# file1.write(str(result['14自摸4'])+' ')
# file1.write(str(result['14榮和1'])+' ')
# file1.write(str(result['14榮和4'])+'\n')
