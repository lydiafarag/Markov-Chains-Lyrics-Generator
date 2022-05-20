# call the APIs, parse the data, and get the raw lyrics from the API calls

# for the credentials
import configparser
from bs4 import BeautifulSoup

# for the API calls; we call the APIs with the request modules
import requests


def getAccessToken():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['Client_Access_Token']['token']  # gives us the token we made in our configuration file


token= getAccessToken(); # save the token as a variable 

#function that allows us to take user input of the artists name for API

def searchArtists(name):
    api_url="https://api.genius.com/search?q={}".format(name)
    headers={"authorization": token} #we need the auth in order for the api request to be satisfied
    r= requests.get(api_url, headers=headers)
    return r.json()


#parse the JSON of the artist and then get the id of the artist 
def getArtistId(name):
    r=searchArtists(name)
    #follow the workflow from the api get request in postman
    id=r["response"]["hits"][0]["result"]["primary_artist"]["id"]
    return id

def getTopSongs(name):
    id=getArtistId(name)
    #call the API to get the top ten songs 
    api_url="https://api.genius.com/artists/{}/songs".format(id)
    headers={"authorization": token} #we need the auth in order for the api request to be satisfied
    #key-value pairs of popularity in base 10
    params= {
        "sort": "popularity",
        "per_page": 10
    }
    r=requests.get(api_url, headers=headers, params=params)
    return r.json()

def getLyrics(name):
    r=getTopSongs(name)
    songs=r["response"]["songs"]
    lyrics_array= [] #intialize an array of all the lyrics 
    #loop thru the songs and parse each one to get the desired output
    for song in songs:
        lyrics_array.append(song["url"])
    return lyrics_array

#now we want to scrape the lyrics to get more functions 

def scrapeLyrics(name):
    links=getLyrics(name)
    lyrics=[]
    for link in links:
        page=requests.get(link)
        soup=BeautifulSoup(page.content, 'html.parser') #new beautiful soup object 

        #after inspecting the web page, we need to target the a tags in the lyrics div 

        lyrics_div=soup.find(class_ ="lyrics")
        lyrics_atags=lyrics_div.find_all("a")
        temp_lyrics=[] # a working list of the lyrics we have scraped 

        #make a list of all lyrics found, append to array, and then put that in the songs_lyrics section

        for tag in lyrics_atags:
            text= tag.text
            temp_lyrics.append(text)
        lyrics.append(temp_lyrics)
    return lyrics

print(scrapeLyrics("drake"))




