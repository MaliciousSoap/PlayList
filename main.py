from asyncio import streams
from email.errors import HeaderParseError
from logging import exception
from os import rename
from tarfile import HeaderError
from tempfile import TemporaryFile
from xml.dom.minidom import Attr
import pytube
from pytube import YouTube
from pytube import Playlist
from mutagen.mp3 import MP3
import shutil
import json
import os
recentlyDownloaded = []

settingsF = open("settings.json")
linksF = open("links.txt","r")

settings = json.load(settingsF)
linksR = linksF.read()

def getLinkConsole():
    url = input("Enter a valid url")
    if url == "":
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    return url.split(",")

def getLinkTxt(rawText):
    noSpaces = rawText.replace(" ","")
    noQuotes = noSpaces.replace('"','')
    linksArr = noQuotes.split(",")
    vidsArr = []
    for link in linksArr:
        if len(link) > 47:
            print("playlist link found")
            playlist = Playlist(link)
            if len(playlist) == 0:
                print(str(link) + " is an empty playlist. Either it is private, deleted, or some other error")
            for link in playlist:
                try:
                    noSpaces = link.replace(" ","")
                    noQuotes = noSpaces.replace('"','')
                    print("appending "+ str(noQuotes))
                    vidsArr.append(noQuotes)
                except AttributeError as e:
                    print("Link cannot be appended because "+ str(e))
        else:
            vidsArr.append(link)
    return vidsArr

def wipeMetadata(fname):
    try:
        file = MP3(fname)
        file.delete()
        file.save()
        print("wiped "+ fname)
    except Exception as e:
        print("could not wipe "+ fname + " due to <" + str(e) + ">")

def download(links):
    for link in links:
        vid = YouTube(link)
        print("downloading " + vid.title)
        soundStreams = vid.streams.filter(only_audio=True)
        firstStream = str(soundStreams[0]).split(" ") #Get first stream
        itag = firstStream[1][6:-1]#Get itag value
        vid.streams.get_by_itag(itag).download()
        fn = ""
        for letter in vid.title:
            if letter in settings['AllowedCharacters']:
                fn += letter
        
        recentlyDownloaded.append(fn+".mp4")
        print("downloaded " + vid.title)

if(settings["JSONInput"]==True):
    download(getLinkTxt(linksR))
elif(settings["JSONInput"]==False):
    download(getLinkConsole())

i=0
for fname in recentlyDownloaded:
    try:
        print("renaming " + fname)
        newName = fname[0:-4]+".mp3"
        rename(fname,newName)
    except FileExistsError:
        print("could not rename file as it already exists")

    if settings["WipeMetadata"] == True:
        wipeMetadata(newName)

    recentlyDownloaded[i] = newName
    i+=1

if settings["FileDirectory"] != "default":
    for fname in recentlyDownloaded:
        try:
            shutil.move(fname,settings["FileDirectory"])
            print("moved "+fname + " to " + settings["FileDirectory"])
        except Exception as e:
            try:
                print(fname + " exists, so was deleted")
                os.replace(settings["FileDirectory"]+"\\"+fname,fname)
                    
                shutil.move(fname,settings["FileDirectory"])
                print("moved "+fname + " to " + settings["FileDirectory"])
            except Exception as e:
                print("could not move file because "+ str(e))
print("exited with code 0")