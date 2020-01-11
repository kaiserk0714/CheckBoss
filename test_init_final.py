# -*- coding: utf-8 -*- 


import asyncio
import discord
import datetime
import threading
import os
'''
import sys 
reload(sys) 
sys.setdefaultencoding('cp949')
'''

basicSetting = []
bossData = []

bossNum = 0

bossTime = []
tmp_bossTime = []

bossTimeString = []
tmp_bossTimeString = []

bossFlag = []
bossMungFlag = []
bossMungCnt = []

client = discord.Client()

channel = ''

def init():
	global basicSetting
	global bossData

	global bossNum

	global bossTime
	global tmp_bossTime

	global bossTimeString
	global tmp_bossTimeString

	global bossFlag
	global bossMungFlag
	global bossMungCnt
	
	tmp_bossData = []
	f = []
	
	inidata = open('test_setting.ini','r', encoding = 'utf-8')

	inputData = inidata.readlines()

	for i in range(inputData.count('\n')):
		inputData.remove('\n')

	basicSetting.append(inputData[0][12:])
	basicSetting.append(inputData[1][15:])
	basicSetting.append(inputData[2][10:])

	for i in range(len(basicSetting)):
		basicSetting[i] = basicSetting[i].strip()
	
	#print (inputData, len(inputData))
	
	bossNum = int((len(inputData)-3)/5)
	
	#print (bossNum)
	
	for i in range(bossNum):
		tmp_bossData.append(inputData[i*5+3:i*5+8])
		
	#print (tmp_bossData)
		
	for j in range(bossNum):
		for i in range(len(tmp_bossData[j])):
			tmp_bossData[j][i] = tmp_bossData[j][i].strip()
	
	for j in range(bossNum):
		tmp_len = tmp_bossData[j][1].find(':')
		f.append(tmp_bossData[j][0][11:])
		f.append(tmp_bossData[j][1][10:tmp_len])
		f.append(tmp_bossData[j][2][13:])
		f.append(tmp_bossData[j][3][20:])
		f.append(tmp_bossData[j][4][13:])
		f.append(tmp_bossData[j][1][tmp_len+1:])
		bossData.append(f)
		f = []
	
	for i in range(bossNum):
		print (bossData[i][0], bossData[i][1], bossData[i][5], bossData[i][2], bossData[i][3], bossData[i][4])
		
	print ('보스젠알림시간 : ', basicSetting[1])
	print ('보스멍확인시간 : ', basicSetting[2])
	
	for i in range(bossNum):
		bossTime.append(datetime.datetime.now()+datetime.timedelta(days=365))
		tmp_bossTime.append(datetime.datetime.now()+datetime.timedelta(days=365))
		bossTimeString.append('99:99:99')
		tmp_bossTimeString.append('')
		bossFlag.append(False)
		bossMungFlag.append(False)
		bossMungCnt.append(0)

init()

nowTimeString = '1'
	
token = basicSetting[0]


async def my_background_task():
	await client.wait_until_ready()

	global channel
	global nowTimeString
	
	global basicSetting
	global bossData

	global bossNum

	global bossTime
	global tmp_bossTime

	global bossTimeString
	global tmp_bossTimeString

	global bossFlag
	global bossMungFlag
	global bossMungCnt
	
	while not client.is_closed:
		now = datetime.datetime.now()
		priv = now+datetime.timedelta(minutes=int(basicSetting[1]))
		privTimeString = priv.strftime('%H:%M:%S')
		nowTimeString = now.strftime('%H:%M:%S')
		aftr = now+datetime.timedelta(minutes=int(0-int(basicSetting[2])))
		aftrTimeString = aftr.strftime('%H:%M:%S')
		#print('loop check ' + bossTime[0].strftime('%H:%M:%S') + ' ' + nowTimeString + ' ' + privTimeString, '	' + aftrTimeString)
		#print('loop check ' + str(bossTime[0]) + ' ' + str(now) + ' ' + str(priv), '	' + str(aftr))

		if channel != '':
			for i in range(bossNum):
				#print (bossData[i][0], bossTime[i])
				if bossTime[i] <= priv:
					if bossFlag[i] == False:
						bossFlag[i] = True
						await client.send_message(channel, bossData[i][0] + ' ' + basicSetting[1] + '분 전 ' + bossData[i][3], tts = True)
						
				if bossTime[i] <= now:
					#print ('if ', bossTime[i])
					'''
					if bossData[i][2] == '1':
						bossMungCnt[i] = 0
					'''
					bossMungFlag[i] = True
					tmp_bossTime[i] = bossTime[i]
					bossTimeString[i] = '99:99:99'
					bossTime[i] = now+datetime.timedelta(days=365)
					await client.send_message(channel, bossData[i][0] + '탐 ' + bossData[i][4], tts = True)
					
				if bossMungFlag[i] == True:
					if (bossTime[i]+datetime.timedelta(days=-365)) <= aftr:
						if bossData[i][2] == '0':
							await client.send_message(channel, bossData[i][0] + ' 미입력 됐습니다.')
							bossFlag[i] = False
							bossMungFlag[i] = False
							bossMungCnt[i] = bossMungCnt[i] + 1
							bossTime[i] = nextTime = now+datetime.timedelta(hours=int(bossData[i][1]), minutes=int(0-int(basicSetting[2])+int(bossData[i][5])))
							tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
							await client.send_message(channel, '다음 ' + bossData[i][0] + ' ' + bossTimeString[i] + '입니다.')
						else :
							await client.send_message(channel, bossData[i][0] + ' 멍 입니다.')
							bossFlag[i] = False
							bossMungFlag[i] = False
							bossMungCnt[i] = bossMungCnt[i] + 1
							bossTime[i] = nextTime = now+datetime.timedelta(hours=int(bossData[i][1]), minutes=int(0-int(basicSetting[2])+int(bossData[i][5])))
							tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
							await client.send_message(channel, '다음 ' + bossData[i][0] + ' ' + bossTimeString[i] + '입니다.')
							
		await asyncio.sleep(1) # task runs every 60 seconds
		

async def joinVoiceChannel():
	channel = client.get_channel("일반")
	await client.join_voice_channel(channel)
	

# 봇이 구동되었을 때 동작되는 코드입니다.
@client.event
async def on_ready():
	print("Logged in as ") #화면에 봇의 아이디, 닉네임이 출력됩니다.
	print(client.user.name)
	print(client.user.id)
	print("===========")

	#await joinVoiceChannel()
	
	client.loop.create_task(my_background_task())
	
	# 디스코드에는 현재 본인이 어떤 게임을 플레이하는지 보여주는 기능이 있습니다.
	# 이 기능을 사용하여 봇의 상태를 간단하게 출력해줄 수 있습니다.
	await client.change_presence(game=discord.Game(name="반갑습니다 :D", type=1))

	
# 봇이 새로운 메시지를 수신했을때 동작되는 코드입니다.
@client.event
async def on_message(message):
	if message.author.bot: #만약 메시지를 보낸사람이 봇일 경우에는
		return None #동작하지 않고 무시합니다.

	global channel
	global nowTimeString

	global basicSetting
	global bossData

	global bossNum

	global bossTime
	global tmp_bossTime

	global bossTimeString
	global tmp_bossTimeString

	global bossFlag
	global bossMungFlag
	global bossMungCnt
	
	id = message.author.id #id라는 변수에는 메시지를 보낸사람의 ID를 담습니다.
	channel = message.channel #channel이라는 변수에는 메시지를 받은 채널의 ID를 담습니다.
	
	modify = ''
	
	hello = message.content
	
	chkpos = hello.find(':')
		
	if hello.find(':') != -1 :
		hours = hello[chkpos-2:chkpos]
		minutes = hello[chkpos+1:chkpos+3]
		now = datetime.datetime.now()
		#print ('oritime', now, 'h', hours, 'm', minutes)
		now = now.replace(hour=int(hours), minute=int(minutes))	
		#print (now)
	else:
		now = datetime.datetime.now()
		nowTimeString = now.strftime('%H:%M:%S')


	for i in range(bossNum):
		if message.content.startswith('!'+ bossData[i][0] +'컷'):
			bossFlag[i] = False
			bossMungFlag[i] = False
			bossMungCnt[i] = 0
			bossTime[i] = nextTime = now+datetime.timedelta(hours=int(bossData[i][1]), minutes= int(bossData[i][5]))
			tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
			await client.send_message(channel, '다음 '+ bossData[i][0] + ' ' + bossTimeString[i] + '입니다.')
			
		if message.content.startswith('!'+ bossData[i][0] +'삭제'):
			bossTime[i] = datetime.datetime.now()+datetime.timedelta(days=365)
			tmp_bossTime[i] =  datetime.datetime.now()+datetime.timedelta(days=365)
			bossTimeString[i] = '99:99:99'
			tmp_bossTimeString[i] = ''
			bossFlag[i] = (False)
			bossMungFlag[i] = (False)
			bossMungCnt[i] = 0
			await client.send_message(channel, '<' + bossData[i][0] + ' 삭제완료>')
			print ('<' + bossData[i][0] + ' 삭제완료>')
		
	if message.content.startswith('!오빠'):
		await client.send_message(channel, '오빠달려려어어어어어어 ', tts=True)
		
	if message.content.startswith('!v') or message.content.startswith('!ㅍ'):
		tmp_sayMessage = message.content
		sayMessage = tmp_sayMessage[3:]
		await client.send_message(channel, "<@" +id+ ">님이 \"" + sayMessage + "\"", tts=True)
	if message.content.startswith('!명치'):
		client.logout()
		client.run(token)
		await client.send_message(channel, '<재접속 성공>')
		print ("<재접속 성공>")
		
	if message.content.startswith('!초기화'):
		basicSetting = []
		bossData = []

		bossTime = []
		tmp_bossTime = []

		bossTimeString = []
		tmp_bossTimeString = []

		bossFlag = []
		bossMungFlag = []
		bossMungCnt = []
		
		init()

		await client.send_message(channel, '<초기화 완료>')
		print ("<초기화 완료>")

	if message.content.startswith('!설정확인'):
		
		setting_val = '보스젠알림시간 : ' + basicSetting[1] + '\n' + '보스멍확인시간 : ' + basicSetting[2] + '\n'
		await client.send_message(channel, setting_val)
		print ('보스젠알림시간 : ', basicSetting[1])
		print ('보스멍확인시간 : ', basicSetting[2])


	if message.content.startswith('!불러오기'):
		try:
			file = open('my_bot.db', 'r')
			beforeBossData = file.readlines()
			
			for i in range(len(beforeBossData)-1):
				for j in range(bossNum):
					if beforeBossData[i+1].find(bossData[j][0]) != -1 :
						tmp_len = beforeBossData[i+1].find(':')

						hours = beforeBossData[i+1][tmp_len+2:tmp_len+4]
						minutes = beforeBossData[i+1][tmp_len+5:tmp_len+7]
						seconds = beforeBossData[i+1][tmp_len+8:tmp_len+10]

						now2 = datetime.datetime.now()

						tmp_now = datetime.datetime.now()
						tmp_now = now.replace(hour=int(hours), minute=int(minutes), second = int(seconds))

						if tmp_now < now2 : 
							deltaTime = datetime.timedelta(hours = int(bossData[j][1]))
							while now2 > tmp_now :
								tmp_now = tmp_now + deltaTime
							now2 = tmp_now
						else :
							now2 = now.replace(hour=int(hours), minute=int(minutes), second = int(seconds))
						bossTime[j] = now2
						bossTimeString[j] = bossTime[j].strftime('%H:%M:%S')
			file.close()
			await client.send_message(channel, '<불러오기 완료>')
			print ("<불러오기 완료>")
		except IOError:
			await client.send_message(channel, '<보스타임 정보가 없습니다.>')
			print ("보스타임 정보가 없습니다.")
	
	if message.content.startswith('!보스탐'):

		for i in range(bossNum):
			for j in range(bossNum):
				if bossTimeString[i] and bossTimeString[j] != '99:99:99':
					if bossTimeString[i] == bossTimeString[j] and i != j:
						tmp_time1 = bossTimeString[j][:6]
						tmp_time2 = (int(bossTimeString[j][6:]) + 1)%100
						#print ('i : ', i, ' ', bossTimeString[i], ' j : ', j, ' ', bossTimeString[j])
						if tmp_time2 < 10 :
							tmp_time22 = '0' + str(tmp_time2)
						elif tmp_time2 == 60 :
							tmp_time22 = '00'
						else :
							tmp_time22 = str(tmp_time2)
						bossTimeString[j] = tmp_time1 + tmp_time22
						#print (bossTimeString[j])

		datelist = bossTimeString
					
		information = '----- 보스탐 정보 -----\n'
		for timestring in sorted(datelist):
			for i in range(bossNum):
				if timestring == bossTimeString[i]:
					if bossTimeString[i] != '99:99:99':
						if bossData[i][2] == '0' :
							if bossMungCnt[i] == 0 :
								information += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + bossTimeString[i] + '\n'
							else :
								information += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + bossTimeString[i] + ' (미입력 ' + str(bossMungCnt[i]) + '회)' + '\n'
						else : 
							if bossMungCnt[i] == 0 :
								information += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + bossTimeString[i] + '\n'
							else :
								information += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + bossTimeString[i] + ' (멍 ' + str(bossMungCnt[i]) + '회)' + '\n'

		await client.send_message(channel, information)
		
		file = open("my_bot.db", 'w')
		file.write(information);
		file.close()
				
	if message.content.startswith('!현재시간'):
		await client.send_message(channel, datetime.datetime.now().strftime('%H:%M:%S'))
access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
