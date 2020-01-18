#   Author: Ryan Guidice
#   Description: Script to automate downloading soundcloud songs and change song metadata for easy iTunes import.

import os
from selenium import webdriver
import requests
import eyed3
import fnmatch
import time

if __name__ == "__main__":
    # Initialization: get target song link from user input, set downloader website and set download directory
    song_link = input("Please enter the soundcloud link: ")
    sc_download_website = 'https://sclouddownloader.net/'
    chrome_options = webdriver.ChromeOptions()
    music_direc = "D:\Ryan\Music"
    prefs = {'download.default_directory':music_direc}
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("log-level=3")
    driver = webdriver.Chrome(options=chrome_options)

    # Get initial list of songs
    file_list = os.listdir("D:\\Ryan\\Music")
    pattern = "*.mp3"
    song_list_1 = []

    for entry in file_list:
        if fnmatch.fnmatch(entry, pattern):
            song_list_1.append(entry)

    # Open Chrome at downloader website
    driver.get(sc_download_website)

    # Find and click the video url textbox, then enter in link
    driver.find_element_by_name("sound-url").click()
    driver.find_element_by_name("sound-url").send_keys(song_link)

    # Click convert button
    driver.find_element_by_class_name("button").click()

    # Delay to let webpage load, then click on the download icon and delay to let file download
    time.sleep(2)
    driver.find_element_by_css_selector(".expanded.button").click()
    time.sleep(10)

    # Detect downloaded file name
    file_list = os.listdir("D:\\Ryan\\Music")
    pattern = "*.mp3"
    song_list_2 = []

    for entry in file_list:
        if fnmatch.fnmatch(entry, pattern):
            song_list_2.append(entry)

    downloaded_song = list(set(song_list_2) - set(song_list_1))
    downloaded_song = downloaded_song[0]

    # Download album art and song metadata
    driver.get(song_link)
    image = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/div/div/div/span").get_attribute("style")
    image = image.split("\"")
    image_url = image[1]

    song_data = driver.title
    long_version = song_data.find("|")
    if long_version == -1:
        song_data = song_data.split(" by ")
    else:
        song_data = song_data[0:len(song_data) - 31].split(" by ")
    song_title = song_data[0]
    song_artist = song_data[1]

    print("Found Title: " + song_title)
    print("Found Artist: " + song_artist)
    user_input = input("Are these accurate? (Y/N): ")
    if user_input == "N" or user_input == "n" or user_input == "No" or user_input == "no":
        song_title = input("Please enter the correct song title: ")
        song_artist = input("Please enter the correct artist: ")
    song_album = input("Please enter the album name: ")

    image_direc = "D:\\Ryan\\Music\\Artwork\\" + song_artist + " - " + song_title + ".jpg"

    with open(image_direc, "wb") as f:
        f.write(requests.get(image_url).content)

    driver.close()

    # Apply album art and song metadata
    song_directory = "D:\\Ryan\\Music\\" + downloaded_song
    song_file = eyed3.load(song_directory)
    song_file.initTag()
    song_file.tag.artist = song_artist
    song_file.tag.title = song_title
    song_file.tag.album = song_album
    if "Single" in song_album or "single" in song_album:
        song_file.tag.track_num = (1,1)
    else:
        song_track_num = input("Track number: ")
        song_track_num_total = input("Total track number: ")
        song_file.tag.track_num = (song_track_num,song_track_num_total)
    image_data = open(image_direc,"rb").read()
    song_file.tag.images.set(3, image_data,"image/jpeg")
    song_file.tag.save()

