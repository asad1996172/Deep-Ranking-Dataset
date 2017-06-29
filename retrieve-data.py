import pandas as pd
import os
import requests
from time import sleep
import random

import socket

proxies = ['96.65.123.249:8118','189.100.80.239:3128','31.11.106.216:3128','144.217.31.225:3128','5.189.189.196:8080','94.41.17.19:53281','200.162.142.178:3128','125.26.99.26:8080','158.69.200.242:3128','82.116.37.13:3128','201.16.140.205:8080','210.207.26.99:8998','36.66.56.130:53281','144.217.241.59:3128','189.1.169.164:3128','35.186.187.230:3128']
count = 3

def download_image(url,fileName,proxy):
    # url = 'http://t3.gstatic.com/images?q=tbn:ANd9GcQOoV-effQLneYh1yuCHEZcJZC4_CbnelSvcodcLjy2bBtEs8Mx'
    # fileName = 'D:\Machine Learning\LUMS work\Reverse Image Search Engine\deep Ranking Technoque\\1.jpg'
    try:
        req = requests.get(url,proxies=proxy)
    except socket.gaierror:
        print('retrying...')
        pr = random.choice(proxies)
        proxyDict = {
            "https": pr,
        }
        download_image(url, fileName, proxyDict)
        return
    except:
        print('retrying...')
        pr = random.choice(proxies)
        proxyDict = {
            "https": pr,
        }
        download_image(url, fileName, proxyDict)
        return

    file = open(fileName, 'wb')
    for chunk in req.iter_content(100000):
        file.write(chunk)
    file.close()


pr = ""
data = open("da.txt")
real_data = data.readlines()
all_data = []
counter=0
for i in range(0,len(real_data),4):
    target = open("done2.txt", 'a')
    if count == 3:
        count =0
        pr = random.choice(proxies)

    proxyDict = {
        "https": pr,
    }



    real_data[i] = real_data[i].replace("\n","")
    real_data[i+1] = real_data[i+1].replace("\n","")
    real_data[i+2] = real_data[i+2].replace("\n","")
    real_data[i+3] = real_data[i+3].replace("\n","")

    print('Downloading Images For ' + real_data[i] + " ...... ")

    if not os.path.exists("dataset2/" + real_data[i] + "_" + str(counter)):
        os.makedirs("dataset2/" + real_data[i] + "_" + str(counter))


    download_image(real_data[i+1],"dataset2/" + real_data[i] + "_" + str(counter) + "/Q.jpg",proxyDict)
    sleep(1)
    count+=1
    print("Query Image Downloaded")
    download_image(real_data[i+2],"dataset2/" + real_data[i] + "_" + str(counter) + "/P.jpg",proxyDict)
    count += 1
    print("Positive Image Downloaded")
    sleep(1)
    download_image(real_data[i+3],"dataset2/" + real_data[i] + "_" + str(counter) + "/N.jpg",proxyDict)
    count += 1
    print("Negative Image Downloaded")
    sleep(1)
    print("downloaded ......\n\n")
    all_data.append({'Text Query': real_data[i], 'Image1': real_data[i+1], 'Image2': real_data[i+2],'Image1_Path': real_data[i]+ "_" + str(counter) + "/Q.jpg",'Image2_Path': real_data[i]+ "_" + str(counter) + "/P.jpg", 'Similarity': 1})
    all_data.append({'Text Query': real_data[i], 'Image1': real_data[i+1], 'Image2': real_data[i+3],'Image1_Path': real_data[i]+ "_" + str(counter) + "/Q.jpg",'Image2_Path': real_data[i]+ "_" + str(counter) + "/N.jpg", 'Similarity': -1})

    target.write(real_data[i])
    target.write("\n")
    target.write(real_data[i + 1])
    target.write("\n")
    target.write(real_data[i + 2])
    target.write("\n")
    target.write(real_data[i + 3])
    target.write("\n")
    target.close()
    print(i)
    counter+=1

all_data = pd.DataFrame(all_data)
if not os.path.isfile('ImageDataSet.csv'):
    all_data.to_csv('ImageDataSet.csv', header='column_names',index=False)
else:  # else it exists so append without writing the header
    all_data.to_csv('ImageDataSet.csv', mode='a', header=False,index=False)