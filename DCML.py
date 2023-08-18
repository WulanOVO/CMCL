from os import path,remove,mkdir,listdir
from shutil import rmtree,unpack_archive
from locale import getdefaultlocale
from psutil import virtual_memory
from subprocess import run
from random import randint
from wget import download
from requests import get
from time import sleep
from json import loads

lang,_ = getdefaultlocale()
lang = lang.lower()

if not path.exists('cmcl.json'):
    name = 'Player'+str(randint(1000,9999))
    if lang == 'zh_cn':
        print('欢迎使用DCML-大聪明启动器！\n你的游戏名是'+name)
    else:
        print('Welcome to use DCML!\nYour player name is '+name)
    sleep(3)
    run('cls',shell=True)

    open('cmcl.json', 'w').write('''{
"exitWithMinecraft": false,
"javaPath": "jdk-20.0.2//bin//java.exe",
"downloadSource": 2,
"checkAccountBeforeStart": false,
"accounts": [{
"playerName": "%s",
"loginMethod": 0,
"selected": true
}],
"printStartupInfo": false,
"maxMemory": 8192
}''' %name)
    download('https://d6.injdk.cn/openjdk/openjdk/20/openjdk-20.0.2_windows-x64_bin.zip')
    unpack_archive('openjdk-20.0.2_windows-x64_bin.zip')
    remove('openjdk-20.0.2_windows-x64_bin.zip')
    download('https://gitee.com/MrShiehX/console-minecraft-launcher/releases/download/2.2/cmcl.jar')
    run('cls',shell=True)

def check():
    global nV
    global nOF
    nV = get('https://download.mcbbs.net/mc/game/version_manifest.json').json()
    nV = nV["latest"]["release"]
    nOF = get('https://download.mcbbs.net/optifine/'+nV,headers={'User-Agent':'Chrome/51.0.2704.63'}).json()
    try:
        nOF = nOF[0]['type']+'_'+nOF[0]['patch']
    except:
        return False
    try:
        old = listdir('.minecraft/versions')[-1].split('-')
        oV = old[0]
        oOF = old[1]
    except:
        return True
    if oV != nV or oOF != nOF:
        return True

if check():
    try:
        rmtree('.minecraft/versions')
        mkdir('.minecraft/versions')
    except:pass
    run('"jdk-20.0.2/bin/java.exe" -jar cmcl.jar install %s --optifine %s -n %s-%s' %(nV,nOF,nV,nOF),shell=True)
    if not path.exists('.minecraft\saves'):
        open('.minecraft\options.txt', 'w').write('lang:'+lang)
    run('cls',shell=True)

try:
    m = loads(open('cmcl.json', 'r').read())
    m["maxMemory"] = virtual_memory().available//1153433
    open('cmcl.json', 'w').write(str(m))
except:pass

run('"jdk-20.0.2/bin/java.exe" -jar cmcl.jar %s-%s' %(nV,nOF),shell=True)
