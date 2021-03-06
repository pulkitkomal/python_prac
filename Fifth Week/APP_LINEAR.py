from tkinter import *
import threading
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats


class linearREG(threading.Thread):
    def url(self):
        lnk = URL1_EN.get()
        link = lnk.replace(' ','-')
        response = requests.get("https://gaana.com/artist/{}".format(link))
        soup = BeautifulSoup(response.text, "html.parser")

        Tags = soup.find_all('body')
        a = str(Tags)
        result = re.findall(r"\w+", a)
        z = result.index('parentnode')
        sourceTAG = result[z + 1]

        durListURL1 = []

        CHTags = soup.find_all('span', class_="parentnode {}".format(sourceTAG))
        for tag in CHTags:
            result = re.findall(r"\w+", tag.text)
            z = result.index('duration')
            dur = result[z + 1]
            s = int(dur)
            if s <= 600:
                durListURL1.append(s)
            else:
                pass

        lnk2 = URL2_EN.get()
        link2 = lnk2.replace(' ', '-')
        response = requests.get("https://gaana.com/artist/{}".format(link2))
        soup = BeautifulSoup(response.text, "html.parser")

        Tags = soup.find_all('body')
        a = str(Tags)
        result = re.findall(r"\w+", a)
        z = result.index('parentnode')
        sourceTAG = result[z + 1]

        durListURL2 = []

        CHTags = soup.find_all('span', class_="parentnode {}".format(sourceTAG))
        for tag in CHTags:
            result = re.findall(r"\w+", tag.text)
            z = result.index('duration')
            dur = result[z + 1]
            s = int(dur)
            if s <= 600:
                durListURL2.append(s)
            else:
                pass
        dataset = list(zip(durListURL1, durListURL2))
        df = pd.DataFrame(data=dataset, columns=["Artist 1", "Artist 2"])
        df.to_csv("1.csv", index=False, header=True)

        print('Artist 1: ')
        for x in durListURL1:
            print(x)


        print('Artist 2:')
        for x in durListURL2:
            print(x)

    def run(self):
        linearREG.url(self)
        space2.config(text = 'OK')


def plotGraph():
    data = pd.read_csv("1.csv")
    X = data["Artist 1"].values
    Y = data["Artist 2"].values

    data = stats.linregress(X,Y)
    b1 = data[0]
    b0 = data[1]

    Y1 = []

    for x in X:
        y = b0 + (b1*x)
        Y1.append(y)


    plt.xlabel('{}'.format(URL1_EN.get()))
    plt.ylabel('{}'.format(URL2_EN.get()))
    plt.grid(True)
    plt.plot(X, Y, "o")
    plt.plot(X, Y1)
    plt.show()


ref = linearREG()


def st():
    ref.start()


root = Tk()

root.title('Data Analysis B/W 2 Artists')
URL1 = Label(root, text='Enter Name of First Artist ').grid(row=0, column=0)
URL1_EN = Entry(root)
URL1_EN.grid(row=0, column=10)

URL2 = Label(root, text='Enter Name of Second Artist ').grid(row=10, column=0)
URL2_EN = Entry(root)
URL2_EN.grid(row=10, column=10)

space1 = Label(root, text='           ').grid(row=20, column=0)

btn = Button(root, text='Submit', command= st).grid(row=30, column=0)
btn2 = Button(root, text='Plot Graph', command= plotGraph).grid(row=30, column=5)

space2 = Label(root, text='       ')
space2.grid(row=50, column=0)



root.resizable(False, False)
root.mainloop()

