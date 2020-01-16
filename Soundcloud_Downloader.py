#   Author: Ryan Guidice
#   Description: Script to automate downloading soundcloud songs and importing them into iTunes

import sys
import os
from selenium import webdriver
import requests
import eyed3
import fnmatch
import time

if __name__ == "__main__":
    #initialization: get target song link from arguments, set downloader website and set download directory
    song_link = 'https://soundcloud.com/user-915717052/brochampton-i-wonder-what-you-are-extended-version'
    sc_download_website = 'https://sclouddownloader.net/'
    chrome_options = webdriver.ChromeOptions()
    music_direc = "D:\Ryan\Music"
    prefs = {'download.default_diretory':music_direc}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=chrome_options)

    # Get initial list of songs
    file_list = os.listdir("D:\\Ryan\\Downloads")
    pattern = "*.mp3"
    song_list_1 = []

    for entry in file_list:
        if fnmatch.fnmatch(entry, pattern):
            song_list_1.append(entry)

    print(song_list_1)

    #open Chrome at downloader website
    driver.get(sc_download_website)

    #find and click the video url textbox, then enter in link
    driver.find_element_by_name("sound-url").click()
    driver.find_element_by_name("sound-url").send_keys(song_link)

    #click convert button
    #driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div[5]/div[1]/div[1]/form/button").click()
    driver.find_element_by_class_name("button").click()

    #delay for 2s to let webpage load, then click on the download icon
    time.sleep(2)
    driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/center/a[1]").click()
    #driver.find_element_by_class_name("expanded button").click()
    time.sleep(10)
    #driver.close()

    #detect downloaded file name
    file_list = os.listdir("D:\\Ryan\\Downloads")
    pattern = "*.mp3"
    song_list_2 = []

    for entry in file_list:
        if fnmatch.fnmatch(entry, pattern):
            song_list_2.append(entry)

    print(song_list_2)

    downloaded_song = list(set(song_list_2) - set(song_list_1))
    downloaded_song = downloaded_song[0]
    print(downloaded_song)

    #download album art and song metadata
    #driver = webdriver.Chrome(options=chrome_options)           # may be unnecessary?
    driver.get(song_link)
    image = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/div/div/div/span").get_attribute("style")
    image = image.split("\"")
    imageurl = image[1]
    print(imageurl)

    song_data = driver.title
    print(song_data)
    long_version = song_data.find("|")
    print(long_version)
    if long_version == -1:
        song_data = song_data.split(" by ")
    else:
        song_data = song_data[0:len(song_data) - 31].split(" by ")
    print(song_data)
    song_title = song_data[0]
    song_artist = song_data[1]

    print("Found Title: " + song_title)
    print("Found Artist: " + song_artist)
    user_input = input("Are these accurate? (Y/N)")
    if user_input == "N" or user_input == "n" or user_input == "No" or user_input == "no":
        song_title = input("Please enter the correct song title:")
        song_artist = input("Please enter the correct artist:")

    image_direc = "D:\\Ryan\\Music\\Artwork\\" + song_artist + " - " + song_title + ".jpg"

    with open(image_direc, "wb") as f:
        f.write(requests.get(imageurl).content)

    driver.close()

    # #apply album art and song metadata
    # song_directory = "D:\\Ryan\\Downloads\\" + downloaded_song
    # song_file = eyed3.load(song_directory)
    # song_file.tag.artist = u"Test Artist"
    # song_file.tag.title = u"Test Title"
    # song_file.tag.save()

