import streamlit as st
import pandas as pd

from googlesearch import search
from bs4 import BeautifulSoup
import requests
import urllib
import re
from pytube import YouTube

geniusLinks = []
azLinks = []
allLinks = []
gaanaLinks = []
jioLinks = []


def getGoogleSearchLinks(query):
    try:
        for links in search(query, tld="co.in", num=10, stop=10, pause=2):
            if "genius" in links:
                geniusLinks.append(links)
            if "azlyrics" in links:
                azLinks.append(links)
            if "jiosaavn" in links:
                jioLinks.append(links)
            if "gaana" in links:
                gaanaLinks.append(links)
            allLinks.append(links)
    except Exception as e:
        print(f"Couldn't find links due to {e}")


def getAZ_info(url):
    try:
        for i in url:
            response = requests.get(i)
            soup = BeautifulSoup(response.content, "html.parser")

            divartist_az = soup.find("div", class_ = "lyricsh")
            if divartist_az:
                artist_az = divartist_az.get_text().replace("Lyrics", "").strip()
            else:
                print("Couldn't find the artist name from AZlyrics :(")
            
            for headings in soup.find_all('h1'):
                song_az = headings.text.replace("lyrics", "").replace('"', '').strip()

        azDic = {}
        if artist_az and song_az:
            azDic[artist_az] = song_az

        return azDic
    except Exception as e:
         print(f"Couldn't handle data from Azlyrics due to: {e}")

         
def getGenius_info(url):
    for i in url:
        response = requests.get(i)
        soup = BeautifulSoup(response.content, "html.parser")

        heading_tags = ["h1"]
        headingCounter = 0
        for tags in soup.find_all(heading_tags):
            if headingCounter < 1:
                genSongName1 = tags.text.strip()
                headingCounter += 1

        divs = soup.find_all('a')

        for i, div in enumerate(divs):
            if i <= 5:
                if i == 5:
                    genArtist1 = div.get_text().strip()
            i += 1
    
    genDic = {}
    if genArtist1 and genSongName1:
        genDic[genArtist1] = (genSongName1).strip(u'\u200b')
    
    return genDic


def getGaana_info(url):
    for i in url:
        response = requests.get(i)
        soup = BeautifulSoup(response.content, "html.parser")

        heading_tags = ["h1"]
        headingCounter = 0
        for tags in soup.find_all(heading_tags):
            if headingCounter < 1:
                getGaana = tags.text.replace('Lyrics', '').strip()
                headingCounter += 1


        divs = soup.find_all('a')

        for i, div in enumerate(divs):
            if i <= 7:
                if i == 7:
                    gaanaArtist = div.get_text().strip()
            i += 1
    gaanaDic = {}
    if gaanaArtist and getGaana:
        gaanaDic[gaanaArtist] = (getGaana).strip(u'\u200b')
    
    return gaanaDic


def getjio_info(url):
    for i in url:
        response = requests.get(i)
        soup = BeautifulSoup(response.content, "html.parser")

        span_tags = ["h1"]
        spanCounter = 0
        for tags in soup.find_all(span_tags):
            getjio_Gaana = tags.text.replace('Lyrics', '').strip()

        divs = soup.find_all('a')
        for i, div in enumerate(divs):
            if i <= 30:
                if i == 30:
                    jioArtist = div.get_text().strip()
            i += 1
        
        jioDic = {}
        if jioArtist and getjio_Gaana:
            jioDic[jioArtist] = (getjio_Gaana).strip(u'\u200b')
        
        return jioDic


def getYTLink_az(azInfo):
    try:
        azKey = str(next(iter(azInfo)))
        azVal = azInfo.get(azKey)
        azYT = f"https://www.youtube.com/results?search_query={azKey} - {azVal}&sp=EgIQAQ%253D%253D"
        return azYT.replace(' ', '')

    except Exception as e:
        st.error(f"Couldn't get the azinfo link due to {e}", icon="🚨")


def getYTLink_gen(genInfo):
    try:
        genKey = str(next(iter(genInfo)))
        genVal = genInfo.get(genKey)

        genYT = f"https://www.youtube.com/results?search_query={genKey} - {genVal}&sp=EgIQAQ%253D%253D"

        return genYT.replace(" ", "")

    except Exception as e:
        st.error(f"Couldn't get the genius link due to {e}", icon="🚨")


def getYTLink_gaana(gaanaInfo):
    try:
        gaanaKey = str(next(iter(gaanaInfo)))
        gaanaVal = gaanaInfo.get(gaanaKey)

        gaanaYT = f"https://www.youtube.com/results?search_query={gaanaKey} - {gaanaVal}&sp=EgIQAQ%253D%253D"
        return gaanaYT.replace(" ", "")

    except Exception as e:
        st.error(f"Couldn't get the gaana link due to {e}", icon="🚨")


def getYTLink_jio(jioInfo):
    try:
        jioKey = str(next(iter(jioInfo)))
        jioVal = jioInfo.get(jioKey)

        jioYT = f"https://www.youtube.com/results?search_query={jioKey} - {jioVal}&sp=EgIQAQ%253D%253D"
        return jioYT.replace(" ", "")

    except Exception as e:
        st.error(f"Couldn't get the jio link due to {e}", icon="🚨")


def getOffYTLink(sName, aName):
    try:
        htmlLink = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + str(sName).replace(' ', '') + "-" + str(aName).replace(' ', ''))
        video_ids = re.findall(r"watch\?v=(\S{11})", htmlLink.read().decode())

        offLink = "https://www.youtube.com/watch?v=" + video_ids[0]
        return offLink

    except Exception as e:
        st.error(f"Couldn't get the official link.", icon="🚨")

def downloadVideo(link, dim):
    if link:
        if dim == 'recommended':
            yt = YouTube(link)
            yt.streams.get_highest_resolution().download()
        elif dim == '360':
            yt = YouTube(link)
            yt.streams.filter(res="360p").first().download()
        elif dim == '720':
            yt = YouTube(link)
            yt.streams.filter(res="720p").first().download()
        elif dim == '480':
            yt = YouTube(link)
            yt.streams.filter(res="480p").first().download()
    
        st.success('video downloaded successfully...')
    
    else:
        st.error("The video can't be downloaded due to no link found.")

def temp(db, link, dim):
    print(db)

st.set_page_config(page_title="MUSICA", page_icon="musical_note")

st.markdown(
    f"""
    <h3 style='color: #300030; font-family: Georgia;'>
        MUSICA &#127925 
    </h3>
    """
    , unsafe_allow_html=True
)


st.sidebar.write(
    f"""
    <h3 style='color: black; font-family: Georgia;'>
        MUSICA &#127925
    </h3>
    """
    , unsafe_allow_html=True
)

st.sidebar.write(
    f"""
    <div style='color: #242B2E; font-family: Roboto;'>
        Type lyrics:
    </div>
    """
    , unsafe_allow_html=True
)

lyricsInput = st.sidebar.text_input("Enter below:", placeholder='Type here')

proceed_button = st.sidebar.button("Enter", key = 'bh')

vidRes = st.sidebar.selectbox('Select Resolution', ('recommended', '720', '480', '360'))

try:
    if proceed_button: 
        if len(lyricsInput) > 0:

            geniusLinks = []
            azLinks = []
            allLinks = []
            gaanaLinks = []
            jioLinks = []
            downloadCheck = False

            st.write(f"""
                <div style='color: green; font-family: Roboto;'>
                    Searching ...
                </div>
                <div style='color: black; font-family: Georgia;'>
                    {lyricsInput}<br>
                </div>
            """
            , unsafe_allow_html=True)

            query = "song lyrics: " + lyricsInput

            getGoogleSearchLinks(query)

            azInfo, azYTLink, = {}, ''
            genInfo, genYTLink, = {}, ''
            gaanaInfo, gaanaYTLink, = {}, ''
            jioInfo, jioYTLink, = {}, ''

            if azLinks:
                azInfo = getAZ_info([azLinks[0]])
                azYTLink = getYTLink_az(azInfo)
            if geniusLinks:
                genInfo = getGenius_info([geniusLinks[0]])
                genYTLink = getYTLink_gen(genInfo)

            if gaanaLinks:
                gaanaInfo = getGaana_info([gaanaLinks[0]])
                gaanaYTLink = getYTLink_gaana(gaanaInfo)

            if jioLinks:
                jioInfo = getjio_info([jioLinks[0]])
                jioYTLinks = getYTLink_jio(jioInfo)

            data = [(song, artist, azYTLink) for artist, song in azInfo.items()] + [(song, artist, genYTLink) for artist, song in genInfo.items()] + [(song, artist, gaanaYTLink) for artist, song in gaanaInfo.items()] + [(song, artist, jioYTLinks) for artist, song in jioInfo.items()]

            infoDF = pd.DataFrame(data, columns=["Song Name", "Artist Name", "YouTube Search"])
            
            if len(infoDF) > 0:
                st.write(f"""
                <h3 style='color: black; font-family: Arial;'>
                    <br>Here's some top result 
                </h3>
                """, unsafe_allow_html=True)
                st.write(infoDF)
                tempDF = infoDF.iloc[:, 0:2]
                song_ = tempDF['Song Name'].values[0]
                artist_ =  tempDF['Artist Name'].values[0]

                offYTLink = getOffYTLink(song_, artist_)
                st.header("YOUTUBE VIDEO")
                st.video(offYTLink)
                db = st.button('Download Video', on_click=downloadVideo, args=(offYTLink, vidRes))

            else:
                st.error('No result found.')
            st.write(f"""
            <div style='color: green; font-family: Roboto;'>
                <br>Not sure what you're looking for? here's a few link to see if you find the desired results
            </div>
            """, unsafe_allow_html=True)
            for i in allLinks:
                st.write(f"""
                        <a href = {i} style='color: blue; font-family: consolas;'>
                            {i}
                        </a>
                        """, unsafe_allow_html=True)
        else:
            st.warning('Please enter Lyrics', icon="⚠️")
except Exception as e:
    st.error(f'Error due to {e}. Please try again.')
