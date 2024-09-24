import os
import speech_recognition as sr
import time
import sys
import ctypes
import wikipedia
import datetime
import json
import re
import webbrowser
import smtplib
import requests
import urllib
import playsound
import urllib.request as urllib2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import strftime
from gtts import gTTS
from youtube_search import YoutubeSearch

language = 'vi'

path = ChromeDriverManager().install()


def speak(text):
    print("Ngọc cute: {}".format(text))
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save("sound.mp3")
    playsound.playsound("sound.mp3", False)
    os.remove("sound.mp3")


def get_voice():
    record = sr.Recognizer()
    with sr.Microphone() as source:
        print("Tôi: ", end='')
        audio = record.listen(source, phrase_time_limit=5)
        try:
            text = record.recognize_google(audio, language="vi-VN")
            print(text)
            return text
        except:
            print("...")
            return 0


def stop():
    speak("Mình chào bạn nhé!")


def get_text():
    for i in range(3):
        text = get_voice()
        if text:
            return text.lower()
        elif i < 2:
            speak("Mình không nghe rõ, bạn có thể nói lại không ?")
    time.sleep(10)
    stop()
    return 0


def talk(name):
    day_time = int(strftime("%H"))
    if day_time < 12:
        speak("Chào buổi sáng {}. Chúc bạn ngày mới tốt lành!".format(name))
    elif day_time < 18:
        speak("Chào buổi chiều {}!".format(name))
    else:
        speak("Chào buổi tối {}!".format(name))


def open_web(text):
    rg = re.search('mở (.+)', text)
    if rg:
        domain = rg.group(1)
        url = "https://www." + domain
        webbrowser.open(url)
        speak("Trang web của bạn đã được mở lên")
        return True
    else:
        return False


def get_time(text):
    now = datetime.datetime.now()
    if "giờ" in text:
        speak("Bây giờ là %d giờ %d phút" % (now.hour, now.minute))
    elif "ngày" in text:
        speak("Hôm nay là ngày %d tháng %d năm %d " % (now.day, now.month, now.year))
    else:
        speak("Mình không hiểu")

def google_search(text):
    search_for = text.split("kiếm", 1)[1]
    speak("Oke")
    driver = webdriver.Chrome()
    driver.get("https://www.google.com")
    query = driver.find_element(By.XPATH,"//*[@id='APjFqb']")
    query.send_keys(str(search_for))
    query.send_keys(Keys.RETURN)
    query.submit()

def main_func():
    speak("""Tôi có thể làm những việc sau:
     1. Chào hỏi
     2. Hiển thị giờ
     3. Mở website
     4. Tìm kiếm trên Google
     5. Dự báo thời tiết
     6. Đọc báo hôm nay
     7. Gửi mail tự động 
     8. Chat GPT
     9. Dịch ngôn ngữ
      """)
    time.sleep(20)


def call():
    speak("Xin chào! Bạn tên là gì nhì? ")
    time.sleep(1)
    name = get_text()
    if name:
        speak("Xin chào {}".format(name))
        time.sleep(3)
        speak("Bạn cần mình giúp gì !")
        time.sleep(2)
        while True:
            text = get_text()
            if not text:
                break
            elif "nói chuyện" in text or "trò chuyện" in text:
                talk(name)
            elif "dừng" in text or "thôi" in text:
                stop()
                break
            elif "mở" in text:
                if "mở google và tìm kiếm" in text:
                    google_search(text)
                else:
                    open_web(text)
            elif "ngày" in text or "giờ" in text:
                get_time(text)


call()
