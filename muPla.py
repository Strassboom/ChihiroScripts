import os, vlc
import youtube_dl
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import shutil
import subprocess

mainLink = "/home/pi/Desktop/ChihiroScripts/"
cuteGirl = "slides"
playSong = "loxinghxn.mp3"
p = vlc.MediaPlayer(playSong)
print(__file__)
print()
while cuteGirl  != "dexd":

	print(os.listdir())
	dirContents = [item for item in os.listdir(mainLink) if not os.path.isdir(item) and item[len(item)-4:] == ".mp3"]
	if cuteGirl == "list":
		for song in dirContents:
			#print(song[len(song)-4:])
			#print(song[-4:0])
			print(" ",song)
	elif cuteGirl == "song":
		fileSearch = input("GiveSong: ")
		playSong = "loxinghxn"
		for elem in dirContents:
			if str.lower(fileSearch) in str.lower(elem):
				p.stop()
				playSong = mainLink+elem
				p = vlc.MediaPlayer(playSong)
				p.play()
				print("now playing: " + playSong)
				break

	elif cuteGirl == "stop":
		if vlc.State._enum_names_[p.get_state()] == "Playing":
			p.stop()
	elif cuteGirl == "pause":
		if vlc.State._enum_names_[p.get_state()] == "Playing":
			p.pause()
	elif cuteGirl == "resume":
		if vlc.State._enum_names_[p.get_state()] == "Paused":
			p.pause()
	elif cuteGirl == "restart":
		p.set_time(0)
	elif cuteGirl == "play":
		p.play()

	elif cuteGirl == "search":
		pulo = input()
		if pulo == "":
			session = HTMLSession()
			searchit = input("Gimme the song name and or artist: ")
			page_link = "https://soundcloud.com/search?q="+searchit.replace(" ","%20")

			r = session.get(page_link)

			choices = [x for x in r.html.absolute_links if "https://soundcloud.com/" in x and x not in ["https://soundcloud.com/","https://soundcloud.com/search","https://soundcloud.com/search/sounds","https://soundcloud.com/search/sets","https://soundcloud.com/search/people","https://soundcloud.com/popular/searches"]]
			if len(choices) > 10:
				choices = choices[:11]
			iterNum = 0
			for item in choices:
				songSearchTitle = BeautifulSoup(requests.get(item).text,"lxml").title.text.split(" |")[0]
				print(" ",iterNum,songSearchTitle if len(songSearchTitle) < 15 else songSearchTitle[:16])
				iterNum += 1
			download = input("Which one or None?")
			try:
				finalChoice = choices[int(download)]
				print(mainLink+BeautifulSoup(requests.get(finalChoice).text,"lxml").title.text)
				ydl_opts = {"outtmpl":mainLink+BeautifulSoup(requests.get(finalChoice).text,"lxml").title.text.split(" |")[0]+".mp3"}
				with youtube_dl.YoutubeDL(ydl_opts) as ydl:
					ydl.download([finalChoice])
			except (IndexError, ValueError):
				print("Not a valid link :(")
				fileSearch = input("GiveSong: ")
				playSong = "loxinghxn"
		elif pulo == "yt":
			searchit = input("Gimme a song name: ")
			page_link = "https://www.youtube.com/results?search_query=" + searchit.replace(" ","+")
			r = requests.get(page_link)
			r = BeautifulSoup(r.content,"html.parser")
			downloadList = []
			downloadHeader = '''https://www.youtube.com'''
			iterNum = 0
			authorList = []
			k = r.find_all("a",{"class":['yt-uix-sessionlink', 'spf-link', '']})
			for x in k:
				authorList.append(x.text)
			whatsThis = r.find_all("a",{"class":['yt-uix-tile-link', 'yt-ui-ellipsis', 'yt-ui-ellipsis-2', 'yt-uix-sessionlink', 'spf-link', ''],"rel":"spf-prefetch"})
			if len(whatsThis) > 10:
				whatsThis = whatsThis[:11]
			for gay in whatsThis:
				foundText = "Unknown Channel"
				mook = gay.find("span").attrs["aria-label"]
				if len(authorList) > 10:
					authorList = authorList[:11]
				for item in authorList:
					if item in mook:
						foundText = item
						break
					print(" ",iterNum,gay.text if len(gay.text) < 15 else gay.text[:15],foundText if len(foundText) < 15 else foundText[:15])

				downloadList.append([gay.text,foundText,gay["href"]])
				iterNum+=1
			try:
				chosenNum = int(input("Select a number entry: "))
				if chosenNum < iterNum:
					ydl_opts = {
                                    'format': 'bestaudio/best',
                                    'postprocessors': [{
                                        'key': 'FFmpegExtractAudio',
                                        'preferredcodec': 'mp3',
                                        'preferredquality': '192',
                                        }],
                                    "outtmpl": mainLink+"%(title)s.%(uploader)s.%(ext)s"
                                }
					with youtube_dl.YoutubeDL(ydl_opts) as ydl:
						ydl.download([downloadHeader+downloadList[chosenNum][2]])
			except:
				print("Nothing Selected")
				pass
	elif cuteGirl == "delete":
		fileSearch = input("As close as you can: ")
		for elem in dirContents:
			if str.lower(fileSearch) in str.lower(elem):
				print(elem+" deleted")
				os.remove(elem)
	elif cuteGirl == "rename":
		fileSearch = input("give guess,newname: ")
		fileNames = fileSearch.split(",")
		for elem in dirContents:
			if str.lower(fileNames[0]) in str.lower(elem):
				print(elem+" is now "+" "+fileNames[1])
				os.rename(elem,fileNames[1])
	elif cuteGirl == "slides":
		#os.chdir("AlterEgoFaces/AlterEgoPC")
		#print(os.listdir())
		os.system("fbi -noverbose -a -t 2 /home/pi/Desktop/ChihiroScripts/AlterEgoFaces/AlterEgoPC/*.png")
		#os.chdir("..")
		#os.chdir("..")
	print()
	cuteGirl = input("muPla: ")
