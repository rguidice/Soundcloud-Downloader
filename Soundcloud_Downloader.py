#   Author: Ryan Guidice
#   Description: Script to automate downloading soundcloud songs and change song metadata for easy iTunes import.

import os
from selenium import webdriver
import requests
import eyed3
import time

if __name__ == "__main__":
    # Initialization: get target song link from user input, set downloader website and set download directory
    song_link = input("Please enter the SoundCloud link: ")
    sc_download_website = "https://sclouddownloader.net/"
    chrome_options = webdriver.ChromeOptions()
    music_directory = "D:\\Ryan\\Music"
    prefs = {"download.default_directory": music_directory}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("log-level=3")
    driver = webdriver.Chrome(options=chrome_options)

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

    downloaded_song = max([music_directory + "\\" + f for f in os.listdir(music_directory)], key=os.path.getctime)

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
    if user_input.lower() == "n" or user_input.lower() == "no":
        song_title = input("Please enter the correct song title: ")
        song_artist = input("Please enter the correct artist: ")
    song_album = input("Please enter the album name: ")

    image_directory = music_directory + "\\Artwork\\" + song_artist + " - " + song_title + ".jpg"

    with open(image_directory, "wb") as f:
        f.write(requests.get(image_url).content)

    driver.close()

    # Apply album art and song metadata
    song_directory = downloaded_song
    song_file = eyed3.load(song_directory)
    song_file.initTag()
    song_file.tag.artist = song_artist
    song_file.tag.title = song_title
    song_file.tag.album = song_album
    if "single" in song_album.lower():
        song_file.tag.track_num = (1, 1)
    else:
        song_track_num = input("Track number: ")
        song_track_num_total = input("Total track number: ")
        song_file.tag.track_num = (song_track_num, song_track_num_total)
    image_data = open(image_directory, "rb").read()
    song_file.tag.images.set(3, image_data, "image/jpeg")
    song_file.tag.save()

