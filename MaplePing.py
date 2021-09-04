import os 
from tcp_latency import measure_latency

print("******************")
print("伺服器         數字")
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
print("上面是每個伺服器對應的數字，請輸入數字來查看伺服器延遲狀況:")
print("(Here is the list of world, please enter a world number)")
w = {0, 1, 2, 3, 4, 6, 45}
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
	
rtt = []
def ping(ch):
	if ch % 2 == 0:
		ch_port = 8585
	else:
		ch_port = 8686
	if ch > 30:
		ip = "202.80.104." + str(((ch - 30) // 2) + 154) # only happens in world 1 
	else:
		ip = "202.80.104." + str((ch//2) + init)
	result = measure_latency(host = ip, port = ch_port)
	if result is None:
		result = 9999999
	print("CH.",ch+1,"= ", round(result[0],3), "ms")
	return round(result[0],3)
	
	
if world == 0: #World 0 has 40 channels
	try:
		for i in range(40):
			rtt.append(ping(i))
	except:
		pass
else:
	try:
		for i in range(30):
			rtt.append(ping(i))
	except:
		pass
		
print("副本: ", round(measure_latency(host = dungeon_ip, port = 8686)[0],3), "ms")
print("商城: ", round(measure_latency(host = mall_ip, port = 8686)[0],3), "ms")

if world != 45: #World Reboot has no Auction system
	print("拍賣: ", round(measure_latency(host = auction_ip, port = 8787)[0],3), "ms")
	  
max_value = max(rtt)
min_value = min(rtt)
print()
print("Maximum delay CH.", rtt.index(max_value)+1, ",RTT = ", max_value, "ms")
print("Minimal delay CH.", rtt.index(min_value)+1, ",RTT = ", min_value, "ms")
print("建議去 CH.",rtt.index(min_value)+1)
print()
os.system("pause")