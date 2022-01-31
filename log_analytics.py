#coding UTF-8

import os, sys, datetime
from collections import deque

#ログファイルと同ディレクトリに配置する必要があります
path= os.getcwd()
path=path+"/"+sys.argv[1]

#ファイル読み込み
with open(path,mode="r", encoding="UTF-8") as f:
	list_log= [file.strip() for file in f.readlines()]

#可変域
N=2
t=900
m=5

#タイムアウトデータ保存用list
list_reftime_timeout= []
list_ipadress_timeout= []
list_times_timeout= []
list_ipadress_timeout_real= []

#サーバーipアドレス保存用list
list_swich= []
list_ipadress_server= [] #二次元配列
list_timeout_server= []

#ping確認用list
list_ping=[]
list_ping_average= [] #二次元配列
list_ping_weight= []
list_ping_weight_time= []

#時間差分計測
def time_difference(variable1, variable2):
	dt1 = datetime.datetime.strptime(str(variable1), '%Y%m%d%H%M%S')
	dt2 = datetime.datetime.strptime(str(variable2), '%Y%m%d%H%M%S')
	return str(dt1-dt2)

#スイッチ別listの作成
for j in range(len(list_log)):
	ip_adress= list_log[j].split(",")[1]
	#スイッチ判別
	ip_adress_swich_split= ip_adress.split(".")[:3]
	ip_adress_swich= '.'.join((str(k) for k in ip_adress_swich_split))
	#スイッチがlistに無い時
	if ip_adress_swich not in list_swich:
		list_swich.append(ip_adress_swich)
		#スイッチ配下サーバーを追記
		list_ipadress_server.append([])
		list_timeout_server.append(0)
		list_ipadress_server[-1].append(ip_adress)

		list_ping.append(ip_adress)

	#スイッチがある時
	else:
		index_number_swich= list_swich.index(ip_adress_swich)
		#新規サーバーなら追記
		if ip_adress not in list_ipadress_server[index_number_swich]:
			list_ipadress_server[index_number_swich].append(ip_adress)

			list_ping.append(ip_adress)

for l in range(len(list_ping)):
	list_ping_size= deque([],m)
	list_ping_average.append(list_ping_size)

#メイン
for i in range(len(list_log)):
	ref_time= list_log[i].split(",")[0]
	ip_adress= list_log[i].split(",")[1]
	ping= list_log[i].split(",")[2]

	#タイムアウトした時
	if list_log[i][-1]== "-" and ip_adress not in list_ipadress_timeout:
		#print(list_log[i].split(",")[0])
		list_ipadress_timeout.append(ip_adress)
		list_reftime_timeout.append(ref_time)
		list_times_timeout.append(0)

	#タイムアウトしているものが復帰した時
	if list_log[i][-1]!= "-" and ip_adress in list_ipadress_timeout:
		index_number_timeout= list_ipadress_timeout.index(ip_adress)
		#復帰出力
		if list_times_timeout[index_number_timeout] >= N:
			print("サーバー復帰　"+ip_adress+"　: "+list_reftime_timeout[index_number_timeout]+"~"+time_difference(ref_time, list_reftime_timeout[index_number_timeout]))
		
		#復帰したサーバーをlist_timeoutから削除
		list_ipadress_timeout.pop(index_number_timeout)
		list_reftime_timeout.pop(index_number_timeout)
		list_times_timeout.pop(index_number_timeout)

		#復帰したスイッチをlistから削除
		if ip_adress in list_ipadress_timeout_real:
			#print(list_ipadress_timeout_real)
			list_ipadress_timeout_real.pop(list_ipadress_timeout_real.index(ip_adress))
			for l in list_swich:
				#print(list_ipadress_timeout_real, list_ipadress_server[list_swich.index(l)])
				if not set(list_ipadress_server[list_swich.index(l)]).issubset(list_ipadress_timeout_real) and list_timeout_server[list_swich.index(l)]!= 0:
					#print(float(ref_time), list_ipadress_timeout_real)
					print("スイッチ復帰　"+l+" : "+list_timeout_server[list_swich.index(l)]+"~"+time_difference(ref_time, list_timeout_server[list_swich.index(l)]))
					list_timeout_server[list_swich.index(l)]= 0

	#連続してタイムアウトした時
	if list_log[i][-1]== "-" and ip_adress in list_ipadress_timeout:
		index_number_timeout= list_ipadress_timeout.index(ip_adress)
		list_times_timeout[index_number_timeout]+=1
		#print(list_times_timeout)

		#タイムアウト出力
		if list_times_timeout[index_number_timeout] >= N and ip_adress not in list_ipadress_timeout_real:
			list_ipadress_timeout_real.append(ip_adress)
			#print(" タイムアウト　"+ip_adress)

			#スイッチ障害
			for k in list_swich:
				#スイッチ配下すべてがタイムアウトしている時
				if set(list_ipadress_server[list_swich.index(k)]).issubset(list_ipadress_timeout_real) and list_timeout_server[list_swich.index(k)]== 0:
					list_timeout_server[list_swich.index(k)]= list_reftime_timeout[list_ipadress_timeout.index(ip_adress)]
					#print("スイッチ障害　"+list_swich[list_swich.index(k)])

	#pingを状態判別listに入力
	index_number_ping= list_ping.index(ip_adress)
	list_ping_average[index_number_ping].append(ping)
	#過負荷状態か判別
	if "-" not in list_ping_average[index_number_ping] and len(list_ping_average[index_number_ping]) == m:
		sum_ping= 0
		for p in range(m):
			sum_ping+= int(list_ping_average[index_number_ping][p])

		if sum_ping/m > t:
			if list_ping[index_number_ping] not in list_ping_weight:
				list_ping_weight.append(list_ping[index_number_ping])
				list_ping_weight_time.append(ref_time)
			#print("　過負荷　　"+list_ping[index_number_ping])

		#過負荷状態が解けた時
		elif list_ping[index_number_ping] in list_ping_weight:
			index_number_ping_time= list_ping_weight.index(list_ping[index_number_ping])

			print("過負荷解消　　"+list_ping[index_number_ping]+ " : "+list_ping_weight_time[index_number_ping_time]+"~"+time_difference(ref_time, list_ping_weight_time[index_number_ping_time]))
			list_ping_weight.pop(index_number_ping_time)
			list_ping_weight_time.pop(index_number_ping_time)


#最後まで復帰していないサーバー出力
for o in range(len(list_ipadress_timeout)):
	if list_times_timeout[o] >= N:
		print("タイムアウト　 "+ list_ipadress_timeout[o]+" : "+list_reftime_timeout[o]+"~")

#最後まで過負荷なサーバー出力
for r in range(len(list_ping_weight)):
		print("　過負荷　　　"+ list_ping_weight[r]+" : "+list_ping_weight_time[r]+"~")

#最後まで復帰しないスイッチ出力
for s in list_swich:
	if list_timeout_server[list_swich.index(s)]!= 0:
		#print(float(ref_time), list_ipadress_timeout_real)
		print("スイッチ障害　"+s+" : "+list_timeout_server[list_swich.index(s)]+"~")


