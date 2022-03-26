from asyncio import streams
from pytube import YouTube
import json
from mutagen.mp3 import MP3

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
    return linksArr

def wipeMetadata(fname):
    file = MP3(fname)
    file.delete()
    file.save()

def download(links):
    for link in links:
        vid = YouTube(link)
        recentlyDownloaded.append([vid.title,link])
        soundStreams = vid.streams.filter(only_audio=True)
        firstStream = str(soundStreams[0]).split(" ") #Get first stream
        itag = firstStream[1][6:-1]#Get itag value
        vid.streams.get_by_itag(itag).download()



if(settings["JSONInput"]==True):
    download(getLinkTxt(linksR))
elif(settings["JSONInput"]==False):
    download(getLinkConsole())


#if(settings["WipeMetadata"]==True):
#    for audioFiles in recentlyDownloaded:
#        wipeMetadata(audioFiles[0])
#        print("wiped successfully")

print("exited with code 0")