import discord
from discord.ext import commands
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from youtube_dl import YoutubeDL
import bs4
from discord.utils import get
from discord import FFmpegPCMAudio
import asyncio
import pyderman as pyderman
from webserver import keep_alive
import os
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import *
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait



app = commands.Bot(command_prefix='!')
voice_client = discord.VoiceClient

user = []
musictitle = []
song_queue = []
musicnow = []
sequence = 0
vc_sound = 0

allplaylist = []

players = {}
queues= {}

def title(msg):
    global music
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chromedriver_autoinstaller.install()   
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.youtube.com/results?search_query="+msg+"+lyrics")
    source = driver.page_source
    bs = bs4.BeautifulSoup(source, 'lxml')
    entire = bs.find_all('a', {'id': 'video-title'})
    entireNum = entire[0]
    music = entireNum.text.strip()
    
    musictitle.append(music)
    musicnow.append(music)
    test1 = entireNum.get('href')
    url = 'https://www.youtube.com'+test1
    with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
    URL = info['formats'][0]['url']
    return music, URL

def play(ctx):
    global vc
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    URL = song_queue[0]
    del user[0]
    del musictitle[0]
    del song_queue[0]
    vc = get(app.voice_clients, guild=ctx.guild)
    if not vc.is_playing():
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))

def play_next(ctx):
    if len(musicnow) - len(user) >= 2:
        for i in range(len(musicnow) - len(user) - 1):
            del musicnow[0]
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    if len(user) >= 1:
        if not vc.is_playing():
            del musicnow[0]
            URL = song_queue[0]
            del user[0]
            del musictitle[0]
            del song_queue[0]
            vc.play(discord.FFmpegPCMAudio(URL,**FFMPEG_OPTIONS), after=lambda e: play_next(ctx))

def again(ctx, url):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
    URL = info['formats'][0]['url']
    if not vc.is_playing():
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after = lambda e: again(ctx, url) )

        
@app.event
async def on_ready():
    print('다음으로 로그인합니다: ')
    print(app.user.name)
    print('connection was succesful')
    await app.change_presence(status=discord.Status.online, activity=discord.Game("음악 연구"))

    
@app.command()
async def 명령어(ctx):
    await ctx.send(embed = discord.Embed(title='명령어',description="""
\n!명령어 -> 뮤직봇의 모든 명령어를 볼 수 있습니다.
\n!들어와 -> 뮤직봇을 자신이 속한 채널로 부릅니다.
\n!나가 -> 뮤직봇을 자신이 속한 채널에서 내보냅니다.
\n!URL재생 [노래링크] -> 유튜브URL를 입력하면 뮤직봇이 노래를 틀어줍니다.
(목록재생에서는 사용할 수 없습니다.)
\n!반복재생 [노래이름] -> 노래를 검색해 반복하여 틀어줍니다. (BETA 버전)
(!나가 명령어가 아닌 이상 노래는 무한반복합니다.)
\n!재생 [노래이름] -> 뮤직봇이 노래를 검색해 틀어줍니다.
(서버 컴퓨터의 성능때문에 약간의 시간이 걸립니다.)
\n!노래끄기 -> 현재 재생중인 노래를 끕니다.
!일시정지 -> 현재 재생중인 노래를 일시정지시킵니다.
!다시재생 -> 일시정지시킨 노래를 다시 재생합니다.
\n!지금노래 -> 지금 재생되고 있는 노래의 제목을 알려줍니다.
\n!멜론차트 -> 최신 멜론차트를 재생합니다.
\n!목록 -> 이어서 재생할 노래목록을 보여줍니다.
!목록재생 -> 목록에 추가된 노래를 재생합니다.
!목록초기화 -> 목록에 추가된 모든 노래를 지웁니다.
\n!대기열추가 [노래] -> 노래를 대기열에 추가합니다.
!대기열삭제 [숫자] -> 대기열에서 입력한 숫자에 해당하는 노래를 지웁니다.
\n!업데이트 -> 점검 후 패치된 내역을 보여줍니다.
!모든패치 -> 지금까지의 업데이트 내역을 전부 보여줍니다.""", color = 0x00ff00))

     
@app.command()
async def 들어와(ctx):
    try:
        global vc
        vc = await ctx.author.voice.channel.connect()   
    except Exception as ex:
        try:
            await vc.move_to(ctx.author.voice.channel)
        except:
            await ctx.send(ex)

@app.command()
async def 나가(ctx):
    try:
        await vc.disconnect()
    except Exception as ex:
        await ctx.send(ex)

@app.command()
async def 재생(ctx, *, msg):
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
    except Exception as ex:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send(ex)
    """
    try:
    """

    if not vc.is_playing():
      global entireText
      YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
      FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

      chrome_options = Options()
      chrome_options.add_argument('--headless')
      chrome_options.add_argument('--no-sandbox')
      chrome_options.add_argument("--single-process")
      chrome_options.add_argument("--disable-dev-shm-usage")
      chromedriver_autoinstaller.install()
      service = Service("chromedriver.exe")   
      driver = webdriver.Chrome(service = service, options=chrome_options)
      driver.get("https://www.youtube.com/results?search_query="+msg+"+lyrics")
      WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="video-title"]'))
        )
      soup = bs4.BeautifulSoup(driver.page_source, 'lxml')
      entire = bs.find_all('a', {'id': 'video-title'})
      entireNum = entire[0]
      entireText = entireNum.text.strip()
      musicurl = entireNum.get('href')
      url = 'https://www.youtube.com'+musicurl
      musicnow.insert(0, entireText)
      with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
      await ctx.send(embed = discord.Embed(title= "노래 재생", description = "현재 " + musicnow[0] + "을(를) 재생하고 있습니다.", color = 0x00ff00))
      await subtitle_song(ctx, url)
      vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after = lambda e: play_next(ctx))
    else:
      user.append(msg)
      result,URLTEST = title(msg)
      song_queue.append(URLTEST)
      await ctx.send("이미 노래가 재생 중이라" + result + "을(를) 대기열로 추가시켰어요!")

@app.command()
async def URL재생(ctx, *, playurl):
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
    except Exception as ex:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send(ex)
    
    if len(musicnow) >= 1:
        if len(user) >= 1:
            pass
        else:
            del musicnow[:]

    global entireText
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    musicnow.insert(0, playurl)
    url = playurl
    
    if not vc.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        vc.is_playing()
        await ctx.send(embed = discord.Embed(title= "노래 재생", description = "현재 " + musicnow[0] + "을(를) 재생하고 있습니다.", color = 0x00ff00))
    else:
        await ctx.send("노래가 이미 재생되고 있습니다!")
    
    
@app.command()
async def 반복재생(ctx, *, msg):
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
    except Exception as ex:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send(ex)
    
    global entireText
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    
    if len(musicnow) - len(user) >= 1:
      for i in range(len(musicnow) - len(user)):
        del musicnow[0]

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chromedriver_autoinstaller.install()   
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.youtube.com/results?search_query="+msg+"+lyrics")
    source = driver.page_source
    bs = bs4.BeautifulSoup(source, 'lxml')
    entire = bs.find_all('a', {'id': 'video-title'})
    entireNum = entire[0]
    entireText = entireNum.text.strip()
    musicnow.insert(0, entireText)
    test1 = entireNum.get('href')
    url = 'https://www.youtube.com'+test1
    await ctx.send(embed = discord.Embed(title= "반복재생", description = "현재 " + musicnow[0] + "을(를) 반복재생하고 있습니다.", color = 0x00ff00))
    again(ctx, url)

@app.command()
async def 일시정지(ctx):
    if vc.is_playing():
        vc.pause()
        await ctx.send(embed = discord.Embed(title= "일시정지", description = musicnow[0] + "을(를) 일시정지 했습니다.", color = 0x00ff00))
    else:
        await ctx.send("지금 노래가 재생되지 않네요.")

@app.command()
async def 다시재생(ctx):
    try:
            vc.resume()
    except:
         await ctx.send("지금 노래가 재생되지 않네요.")
         
    else:
         await ctx.send(embed = discord.Embed(title= "다시재생", description = musicnow[0] + "을(를) 다시 재생했습니다.", color = 0x00ff00))

@app.command()
async def 노래끄기(ctx):
    if vc.is_playing():
        vc.stop()
        await ctx.send(embed = discord.Embed(title= "노래끄기", description = musicnow[0] + "을(를) 종료했습니다.", color = 0x00ff00))
    else:
        await ctx.send("지금 노래가 재생되지 않네요.")

@app.command()
async def 지금노래(ctx):
    if not vc.is_playing():
        await ctx.send("지금 노래가 재생되지 않네요.")
    else:
        await ctx.send(embed = discord.Embed(title= "지금노래", description = "현재 " + musicnow[0] + "을(를) 재생하고 있습니다.", color = 0x00ff00))
    
@app.command()
async def 멜론차트(ctx):
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
    except:
        pass
    
    global entireText
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--disable-dev-shm-usage")

    chromedriver_autoinstaller.install()   
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.youtube.com/results?search_query=멜론차트")
    source = driver.page_source
    bs = bs4.BeautifulSoup(source, 'lxml')
    entire = bs.find_all('a', {'id': 'video-title'})
    entireNum = entire[0]
    entireText = entireNum.text.strip()
    musicnow.insert(0, entireText)
    test1 = entireNum.get('href')
    url = 'https://www.youtube.com'+test1

    if not vc.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        vc.is_playing()
        await ctx.send(embed = discord.Embed(title= "노래 재생", description = "현재 " + musicnow[0] + "을(를) 재생하고 있습니다.", color = 0x00ff00))
    else:
        await ctx.send("노래가 이미 재생되고 있습니다!")    
    
    
@app.command()
async def 대기열추가(ctx, *, msg):
    user.append(msg)
    result, URLTEST = title(msg)
    song_queue.append(URLTEST)
    await ctx.send(result + "를 재생목록에 추가했어요!")

@app.command()
async def 대기열삭제(ctx, *, number):
    try:
        ex = len(musicnow) - len(user)
        del user[int(number) - 1]
        del musictitle[int(number) - 1]
        del song_queue[int(number)-1]
        del musicnow[int(number)-1+ex]
            
        await ctx.send("대기열이 정상적으로 삭제되었습니다.")
    except:
        if len(list) == 0:
            await ctx.send("대기열에 노래가 없어 삭제할 수 없어요!")
        else:
            if len(list) < int(number):
                await ctx.send("숫자의 범위가 목록개수를 벗어났습니다!")
            else:
                await ctx.send("숫자를 입력해주세요!")

@app.command()
async def 목록재생(ctx):
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
    except:
        pass
    
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    
    if len(user) == 0:
        await ctx.send("아직 아무노래도 등록하지 않았어요.")
    else:
        if len(musicnow) - len(user) >= 1:
            for i in range(len(musicnow) - len(user)):
                del musicnow[0]
        play(ctx)

        

@app.command()
async def 목록(ctx):
    if len(musictitle) == 0:
        await ctx.send("아직 아무노래도 등록하지 않았어요.")
    else:
        global Text
        Text = ""
        for i in range(len(musictitle)):
            Text = Text + "\n" + str(i + 1) + ". " + str(musictitle[i])
            
        await ctx.send(embed = discord.Embed(title= "노래목록", description = Text.strip(), color = 0x00ff00))

@app.command()
async def 목록초기화(ctx):
    try:
        ex = len(musicnow) - len(user)
        del user[:]
        del musictitle[:]
        del song_queue[:]
        while True:
            try:
                del musicnow[ex]
            except:
                break
        await ctx.send(embed = discord.Embed(title= "목록초기화", description = """
목록이 정상적으로 초기화되었습니다.
이제 노래를 등록해볼까요?""", color = 0x00ff00))
    except:
        await ctx.send("아직 아무노래도 등록하지 않았어요.")
