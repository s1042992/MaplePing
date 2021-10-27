import os
from tcp_latency import measure_latency
import numpy as np

channel_rtt = np.array(range(40), np.float)
withoutfb_cnt = 0
def get_ip(ch):
	if ch > 30:
		ip = "202.80.104." + str(((ch - 30) // 2) + 154) # only happens in world 0 
	else:
		ip = "202.80.104." + str((ch // 2) + init)
	return ip
	
def get_port(ch):
	if ch % 2 == 0:
		return 8585
	else:
		return 8686
def ping_job(channel):
	result = measure_latency(host = get_ip(channel), port = get_port(channel), timeout=2.5)
	#print(result[0])
	if result[0] is None:
		result[0] = 999999
		global withoutfb_cnt
		withoutfb_cnt = withoutfb_cnt + 1
		
	channel_rtt[channel] = round(result[0],3)
	print("CH.", channel + 1,"= ", channel_rtt[channel], "ms")

	
if __name__ == '__main__':
	print("******************")
	print("伺服器         編號")
	print()
	print("艾麗亞:   	 0")
	print("普力特:   	 1")
	print("琉德:     	 2")
	print("優依娜:   	 3")
	print("愛麗西亞: 	 4")
	print("殺人鯨:   	 6")
	print("Reboot:		45")
	print()
	print("******************")
	print("上面是每個伺服器對應的編號，請輸入編號來查看本機與伺服器之間延遲狀況:")
	
	w = {0, 1, 2, 3, 4, 6, 45}
	while True:
		print()
		print("上面是每個伺服器對應的編號，請輸入編號來查看本機與伺服器之間延遲狀況:")
		print("(Please enter a world number based on the list above.)")
		channel_rtt = np.array(range(40), np.float)
		withoutfb_cnt = 0
		while True:
			world = input()
			try:
				world = int(world)
				if world in w:
					print("Please wait for a while...")
					break
				else:
					print("Please re-enter a legal world number:")
					continue
			except:
				print("Please re-enter a legal world number:")
				continue
			
		if world == 6: # there's no world 5
			world = world - 1

		if world == 45: #World Reboot is very special...
			init = 164
			dungeon_ip = "202.80.104.39"
			mall_ip = "202.80.104.47"
		else:
			init = 64 + world * 15
			dungeon_ip = "202.80.104." + str(32 + world)
			mall_ip = "202.80.104." + str(40 + world)
			auction_ip = "202.80.104." + str(40 + world)
			
		if world == 0: #World 0 has 40 channels
			try:
				for i in range(40):
					ping_job(i)
					
			except:
				pass
		else:
			try:
				for i in range(30):
					ping_job(i)
			except:
				pass
		
		result_dungeon = measure_latency(dungeon_ip, 8686)[0]
		result_mall = measure_latency(mall_ip, 8686)[0]
		
		if result_dungeon is None:
			print("副本: 9999999.0 ms")
		else:
			print("副本: ", round(result_dungeon, 3), "ms")
			
		if result_mall is None:
			print("商城: 9999999.0 ms")
		else:	
			print("商城: ", round(result_mall, 3), "ms")

		if world != 45: #World Reboot has no Auction system
			result_auction = measure_latency(auction_ip, 8686)[0]
			if result_auction is None:
				print("拍賣: 9999999.0 ms")
			else:
				print("拍賣: ", round(measure_latency(auction_ip, 8787)[0],3), "ms")

		channel_rtt = channel_rtt.tolist()
		if world != 0:	 
			max_value = max(channel_rtt[0:30])
			min_value = min(channel_rtt[0:30])
		else:
			max_value = max(channel_rtt)
			min_value = min(channel_rtt)

		if withoutfb_cnt > 15:
			print("伺服器可能在維修中或是掛了")
		else:
			print()
			print("Maximum delay CH.", channel_rtt.index(max_value)+1, ",RTT = ", max_value, "ms")
			print("Minimal delay CH.", channel_rtt.index(min_value)+1, ",RTT = ", min_value, "ms")
			print("建議去 CH.",channel_rtt.index(min_value)+1)
			print()
	os.system("pause")