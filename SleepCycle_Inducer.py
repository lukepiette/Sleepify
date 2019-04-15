
# coding: utf-8

# In[1]:


import struct
import socket
import codecs
import time
from pygame import mixer
import matplotlib.pyplot as plt
import random


# In[2]:


def _getDecDigit(digit):
    digits = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
    for x in range(len(digits)):
        if digit.lower() == digits[x]:
            return(x)
        
def hexToDec(hexNum):
    decNum = 0
    power = 0

    for digit in range(len(hexNum), 0, -1):
        try:
            decNum = decNum + 16 ** power * _getDecDigit(hexNum[digit-1])
            power += 1
        except:
            return
    return(int(decNum))


# In[3]:


UDP_IP = "10.165.0.207"
UDP_PORT = 6092

sock = socket.socket(socket.AF_INET,  # Internet
                    socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))

final = []
latest = []
count = 0
luo = 0


# In[ ]:


print('Program Initiated')
while True:
    
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    if 'alpha_absolute' in str(data):
        
        newData = str(data).split(",")
        newData = newData[1].split("x")
        newData = newData[1:]
        out = [hexToDec(i[:-1]) for i in newData]
        NewOut = []
        
        for i in out:
            if i != None and i != 0:
                NewOut += [i]
                        
        latest += [sum(NewOut)]   
        count += 1
        luo += 1

        if count > 10:
            count = 0
            final += [sum(latest)]
            latest = []
            print(final[-1], luo)
            
        if luo > 3000:
            break
            
            
out = []
for i in final:
    if i < 80000:
        out += [i]

plt.rcParams["figure.figsize"] = (20,5)
plt.plot([i for i in range(len(out))],out)
plt.plot([i for i in range(len(out))],[28000 for i in range(len(out))])


# In[5]:


def play_func(num):
    
    mixer.init()
    
    if num == 1:
        white_list = ["Downloads\white_1.mp3","Downloads\white_2.mp3","Downloads\white_3.mp3","Downloads\white_4.mp3"]
        mixer.music.load(white_list[random.randint(0,3)])
        mixer.music.play()
        
    if num == 2:
        pink_list = ["Downloads\pink_1.mp3","Downloads\pink_2.mp3","Downloads\pink_3.mp3","Downloads\pink_3.mp3"]
        mixer.music.load(pink_list[random.randint(0,3)])
        mixer.music.play()
        
    if num == 3:
        ASMR_list = ["Downloads\ASMR_1.mp3","Downloads\ASMR_2.mp3","Downloads\ASMR_3.mp3","Downloads\ASMR_4.mp3"]
        mixer.music.load(ASMR_list[random.randint(0,3)])
        mixer.music.play()
        
    if num == 4:
        Animal_list = ["Downloads\Animal_1.mp3","Downloads\Animal_2.mp3","Downloads\Animal_3.mp3","Downloads\Animal_4.mp3"]
        mixer.music.load(Animal_list[random.randint(0,3)])
        mixer.music.play()
        
    if num == 5:
        soft_music_list = ["Downloads\soft_music_1.mp3","Downloads\soft_music_2.mp3","Downloads\soft_music_3.mp3","Downloads\soft_music_4.mp3"]
        mixer.music.load(soft_music_list[random.randint(0,3)])
        mixer.music.play()
        
    if num == 6:
        water_list = ["Downloads\water_1.mp3","Downloads\water_2.mp3","Downloads\water_3.mp3","Downloads\water_4.mp3"]
        mixer.music.load(water_list[random.randint(0,3)])
        mixer.music.play()


# In[6]:


def waves(num, name):
    count = 0
    final = []
    
    while count < num:
        count += 1
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        
        if '{}_absolute'.format(name) in str(data):
            newData = str(data).split(",")
            newData = newData[1].split("x")
            newData = newData[1:]
            out = [hexToDec(i[:-1]) for i in newData]
            NewOut = []

            for i in out:
                if i != None and i != 0:
                    NewOut += [i]

            final += [sum(NewOut)]
            
    out = []
    for i in final:
        if i < 80000:
            out += [i]
    
    return(sum(out)/len(out))


# In[7]:


def cycle(cycles, name):
    
    mixer.init()
    full_list = []
    num = 0

    while num < 6:
        num += 1
        play_func(num)
        full_list += [waves(cycles, name)]
        mixer.quit()
        time.sleep(4)
    
    return([full_list.index(min(full_list)), min(full_list)])


# In[8]:


def monitor_up(join,tic,name):
    
    data = []
    spin = 100000000
    numy = 0
    mixer.init()
    mixer.quit()
    start_level = waves(join, name)
    
    while True:
        numy += 1
        base_level = waves(join, name)
        
        if (base_level*0.75) > start_level:
            break
        
        if spin > base_level:
            music_played = cycle(join, name)
            music_level = music_played[1]
            music_number = music_played[0]
        
            if music_level > base_level:
                play_func(music_number)
                data += [["rot:{}".format(numy), "sound: {}".format(music_number)]]
            else:
                data += [["rot:{}".format(numy), "no switch"]]
                
            spin = music_level
        time.sleep(tic)
        
    return(data)


# In[9]:


def monitor_down(join,tic, name):
    
    data = []
    spin = 0
    numy = 0
    mixer.init()
    mixer.quit()
    start_level = waves(join, name)
    
    while True:
        numy += 1
        base_level = waves(join, name)
        
        if (base_level*1.25) < start_level:
            break
        
        if spin < base_level:
            music_played = cycle(join, name)
            music_level = music_played[1]
            music_number = music_played[0]
        
            if music_level < base_level:
                play_func(music_number)
                data += [music_number, "rot:{}".format(numy), "sound: {}".format(music_number)] 
            else:
                data += ["no switch", "rot:{}".format(numy)]
                
            spin = music_level
        time.sleep(tic)
        
    return(data)


# In[113]:


def full_sleep(spinz, tim):
    
    ## Into Deep Sleep
    beta_data = monitor_down(spinz, tim, "beta")
    print("stage 1")
    alpha_data = monitor_down(spinz, tim, "alpha")
    print("stage 2")
    theta_data = monitor_up(spinz, tim, "theta")
    print("stage 3")
    delta_data = monitor_up(spinz, tim, "delta")
    print("stage 4")
    
    time.sleep(1200)
    
    ## Out of Deep Sleep
    delta_data_up = monitor_down(spinz, tim, "delta")
    theta_data_up = monitor_down(spinz, tim, "theta")
    alpha_data_up = monitor_up(spinz, tim, "alpha")
    beta_data_up = monitor_up(spinz, tim, "beta")
    
    ## Data Collection
    down_data = [beta_data, alpha_data, theta_data, delta_data]
    up_data = [beta_data_up, alpha_data_up, theta_data_up, delta_data_up]
    
    return([down_data, up_data])    


# In[ ]:


full_sleep(15000,10)

