import os
import time 
from tcp_latency import measure_latency
import numpy as np

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
print("(Here is the list of world, please enter a world number)")
w = {0, 1, 2, 3, 4, 6, 45}

def get_ip(ch):
	if ch > 30:
		ip = "202.80.104." + str(((ch - 30) // 2) + 154) # only happens in world 0 
	else:
		ip = "202.80.104." + str((ch // 2) + init)
	return ip
	
def get_port(ch):
	if i % 2 == 0:
		return 8585
	else:
		return 8686
		
if __name__ == '__main__':
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
		
	channel_rtt = np.array(range(40), np.float)	
	thread = []
	if world == 0: #World 0 has 40 channels
		try:
			for i in range(40):
				result = measure_latency(get_ip(i), get_port(i))
				if result is None:
					result = 999999	
				print("CH.", i+1,"= ", round(result[0],3), "ms")
				channel_rtt[i] = round(result[0],3)

		except:
			pass
	else:
		try:
			for i in range(30):
				result = measure_latency(get_ip(i), get_port(i))
				if result is None:
					result = 999999	
				print("CH.", i+1,"= ", round(result[0],3), "ms")
				channel_rtt[i] = round(result[0],3)
		except:
			pass

	print("副本: ", round(measure_latency(dungeon_ip, 8686)[0],3), "ms")
	print("商城: ", round(measure_latency(mall_ip, 8686)[0],3), "ms")

	if world != 45: #World Reboot has no Auction system
		print("拍賣: ", round(measure_latency(auction_ip, 8787)[0],3), "ms")

	channel_rtt = channel_rtt.tolist()
	if world != 0:	 
		max_value = max(channel_rtt[0:30])
		min_value = min(channel_rtt[0:30])
	else:
		max_value = max(channel_rtt)
		min_value = min(channel_rtt)

	print()
	print("Maximum delay CH.", channel_rtt.index(max_value)+1, ",RTT = ", max_value, "ms")
	print("Minimal delay CH.", channel_rtt.index(min_value)+1, ",RTT = ", min_value, "ms")
	print("建議去 CH.",channel_rtt.index(min_value)+1)
	print()
	os.system("pause")