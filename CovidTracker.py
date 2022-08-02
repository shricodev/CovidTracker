"""
Simple tool written in Python using (https://worldometers.info) to get updates of COVID-19 cases in real time.
Supports notification system to give updates in 3-hours interval.

Author: Shrijal Achärya (~YuShx01)
"""

import sys
import requests
from bs4 import BeautifulSoup
import pyfiglet

result = pyfiglet.figlet_format("Corona Update", font="rectangles")
print(result)
print(
    "\033[95m Note: This tool solely relies on Worldometer and its data, so data's change only after change in Worldometer.\n\033[0m"
)

country = input(
    "Enter the country name to see the data of COVID-19 cases alltime/today: "
).lower()

if country == '':
    print('Invalid Input!')
    sys.exit()
    
url = "https://worldometers.info/coronavirus" + "/country/" + country
# print(url)
head_req = requests.get(url, allow_redirects=True)
ls4 = []

if head_req.url == "https://www.worldometers.info/404.shtml":
    print("Enter correct country name. Check your input!")
    sys.exit()

response = requests.get("https://iconarchive.com/download/i88232/icons8/ios7/Healthcare-Virus.ico")

file = open("sample_image.ico", "wb")
file.write(response.content)
file.close()


def get_data():
    global ls
    global ls3
    global ls4
    global ls1
    global url
    global parsed

    superscript = str.maketrans("zZz", "ᶻZᶻ")
    try:
        getReq = requests.get(url)
        contents = getReq.content
        parsed = BeautifulSoup(contents, "html.parser")
        all = parsed.findAll("div", class_="maincounter-number")

        ls = [i.get_text() for i in all]

        ls1 = [i.strip("\n") for i in ls]
        todayUpdate = parsed.findAll("li", class_="news_li")
        ls2 = [i.get_text() for i in todayUpdate]

        ls3 = [i.split("[source]") for i in ls2]

        for items in ls3:
            if items != "":
                ls4.append(items)

    except Exception as e:
        print(e)


def notifications(userInput):
    import ssl
    import time

    # global ls4
    from plyer import notification
    # from urllib.request import urlretrieve

    ls2 = []
    ssl._create_default_https_context = ssl._create_unverified_context
    # imgGet = urlretrieve(
    #     "https://iconarchive.com/download/i88232/icons8/ios7/Healthcare-Virus.ico",
    #     r"C:\Windows\Temp\sample.ico",
    # )
    # url = 'https://iconarchive.com/download/i88232/icons8/ios7/Healthcare-Virus.ico'

    todayUpdate = parsed.findAll("li", class_="news_li")
    ls2 = [i.get_text() for i in todayUpdate]
    ls3 = [i.split("[source]") for i in ls2]

    while True:
        notification.notify(
            title=f"Coronavirus Update: {country.upper()} Today",
            message=f"Today's Cases: {ls4[0][0]}",
            app_icon="sample_image.ico",
            timeout=15,
        )
        time.sleep(10800)


def one_time():
    from plyer import notification

    print("-" * 60)
    print(f"|\t\tTotal Coronavirus Case Study in {country.upper()}")
    print("-" * 60)
    print(f"|Total Case: {ls1[0]}")
    print("-" * 60)
    print(f"|Total Death: {ls1[1]}")
    print("-" * 60)
    print(f"|Total Recovered: {ls1[2]}")
    print("-" * 60)
    print("\n")

    print("-" * 90)
    print(f"|\t\tToday's Coronavirus Case Study in {country.capitalize()}")
    print("-" * 90)
    print(f"|Today: {ls3[0][0]}")
    print("-" * 90)
    print(f"|Yesterday: {ls3[1][0]}")
    print("-" * 90)
    print(f"|Day before yesterday: {ls3[2][0]}")
    print("-" * 90)

    notification.notify(
        title=f"Coronavirus Update: {country.upper()}",
        message=f"Total Cases: {ls1[0]}, Deaths: {ls1[1]} and recovered: {ls1[2]}",
        app_icon="sample_image.ico",
        timeout=15,
    )


if __name__ == "__main__":
    get_data()
    one_time()
    print("\n")
    userInput = input(
        "Do you want to get notification from the program (3-hours time interval) [Y/N]: "
    )
    if userInput != "y" and userInput != "Y":
        sys.exit()
    else:
        notifications(userInput)
