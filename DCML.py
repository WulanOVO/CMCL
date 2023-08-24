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

#获取系统语言#
lang,_ = getdefaultlocale()
lang = lang.lower()

if not path.exists('cmcl.json'): #判断第一次启动#
    #生成玩家名#
    name = 'Player'+str(randint(1000,9999))
    if lang == 'zh_cn':
        print('欢迎使用DCML-大聪明启动器！\n你的游戏名是'+name)
    else:
        print('Welcome to use DCML!\nYour player name is '+name)
    sleep(3)
    run('cls',shell=True)

    try:
        #下载Java并解压#
        download('https://d6.injdk.cn/openjdk/openjdk/20/openjdk-20.0.2_windows-x64_bin.zip')
        unpack_archive('openjdk-20.0.2_windows-x64_bin.zip')
        remove('openjdk-20.0.2_windows-x64_bin.zip')
        #下载cmcl#
        download('https://gitee.com/MrShiehX/console-minecraft-launcher/releases/download/2.2/cmcl.jar')
    except:
        #无网络时报错并退出#
        if lang == 'zh_cn':
            print('下载出错，请检测网络或稍后重试')
        else:
            print('Download error, please check the network or try again later')
        sleep(3)
        exit(0)

    #手动创建cmcl.json#
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
    run('cls',shell=True)

def check(): #检测是否需要更新#
    global nV
    global nOF
    h = {'User-Agent':'Chrome/51.0.2704.63'}
    first = False
    noOF = False
    vL = []

    #获取游戏正式版列表#
    nV = get('https://download.mcbbs.net/mc/game/version_manifest.json',headers=h).json()
    for i in range(len(nV["versions"])):
        if nV["versions"][i]["type"] == "release": #筛选类型是正式版的版本#
            vL.append(nV["versions"][i]["id"]) #版本号加入列表#
    nV = vL[0] #获取版本列表第一项（最新版本）#

    #根据最新版本获取OF版本#
    nOF = get('https://download.mcbbs.net/optifine/'+nV,headers=h).json()
    try:
        nOF = nOF[0]['type']+'_'+nOF[0]['patch']
    except:
        noOF = True #标记没有OF（OF没更新）#

    #获取现有的游戏版本和OF#
    try:
        old = listdir('.minecraft/versions')[-1] #读取versions里的最后一个文件名#
        old = old.split('-') #通过“-”区分游戏版本和OF#
        oV = old[0]
        oOF = old[1]
    except:
        first = True #标记第一次启动（没有以安装版本）#

    if first and noOF: #第一次启动&OF没更新#
        nV = vL[1] #下载版本改为上一个版本#
        nOF = nOF[0]['type']+'_'+nOF[0]['patch'] #重新获取OF版本#
        return True
    elif first and not noOF: #第一次启动&有OF#
        return True
    elif not first and noOF: #不是第一次启动&OF没更新#
        return False #不更新，等待OF更新新版本#

    if oV != nV or oOF != nOF: #常规判断#
        return True


if check():
    try:
        #删除旧版本（不影响存档）#
        rmtree('.minecraft/versions')
        mkdir('.minecraft/versions')
    except:pass
    #下载新版本（命名格式：游戏版本-OF版本）#
    run('"jdk-20.0.2/bin/java.exe" -jar cmcl.jar install %s --optifine %s -n %s-%s' %(nV,nOF,nV,nOF),shell=True)

    if not path.exists('.minecraft\saves'): #判断第一次下载#
        open('.minecraft\options.txt', 'w').write('lang:'+lang) #自动修改游戏语言#

    run('cls',shell=True)

try:
    #自动分配内存#
    m = loads(open('cmcl.json', 'r').read())
    m["maxMemory"] = virtual_memory().available//1153433 #获取可用内存并修改cmcl.json#
    open('cmcl.json', 'w').write(str(m))
except:pass

#我的世界，启动！#
run('"jdk-20.0.2/bin/java.exe" -jar cmcl.jar %s-%s' %(nV,nOF),shell=True)
