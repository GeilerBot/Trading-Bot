import requests
import json
import time
import random
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}


def getShoeNumber():
    while True: 
        res = requests.get("https://www.snipes.com/c/shoes/sneaker?openCategory=true&sz=502", headers=headers)
        print(res.status_code)
        soup = BeautifulSoup(res.content, 'html.parser')

        dataListResults = soup.find('script')

        df = open("Monitor-Bot\\res.txt", "w")
        df.write(str(dataListResults))
        df.close()
        df = open("Monitor-Bot\\res.txt", "r")
        read = df.read()
        df.seek(0)
        read

        arr = []
        line = 1
        for word in read:
            if word == '\n':
                line += 1
        for i in range(line):
            arr.append(df.readline())

        def findline(word):
            for i in range(len(arr)):
                if word in arr[i]:
                    print(i+1)

        shoesLine = findline("listResults:")

        resultsArr = arr[15]

        str1 = ""

        for word in resultsArr:
            str1 += word

        str1 = str1.strip()
        str1 = str1.replace("listResults:", "")
        str1 = str1.replace(" ", "")
        str1 = str1.replace(",", "")
        numberOfShoe = int(str1)
        print(numberOfShoe)
        if numberOfShoe > 502:
            print("New Shoe Loaded! \n Number of Shoes now: ",numberOfShoe)
        randInteger = random.randint(26, 30)
        time.sleep(randInteger)

getShoeNumber()


