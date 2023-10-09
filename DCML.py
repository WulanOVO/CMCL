from os import path,remove,mkdir,listdir,system
from shutil import rmtree,unpack_archive
from locale import getdefaultlocale
from psutil import virtual_memory
from random import randint
from wget import download
from requests import get
from json import loads

#获取系统语言#
lang,_ = getdefaultlocale()
lang = lang.lower()
system('cls')

#初始化#
if not path.exists('cmcl.json'): #判断第一次启动#
    #生成玩家名#
    name = 'Player'+str(randint(1000,9999))
    if lang == 'zh_cn':
        print('欢迎使用DCML-大聪明启动器！\n你的游戏名是'+name)
    else:
        print('Welcome to use DCML!\nYour player name is '+name)

    #下载cmcl#
    download('https://gitee.com/MrShiehX/console-minecraft-launcher/releases/download/2.2.1/cmcl.jar',bar=None)
    system('cls')

    try:
        #下载Java并解压#
        download('https://d6.injdk.cn/openjdk/openjdk/21/openjdk-21_windows-x64_bin.zip')
        unpack_archive('openjdk-21_windows-x64_bin.zip')
        remove('openjdk-21_windows-x64_bin.zip')
    except:
        #无网络时报错并退出#
        if lang == 'zh_cn':
            print('下载出错，请检测网络或稍后重试')
        else:
            print('Download error, please check the network or try again later')
        while True:pass

    #手动创建cmcl.json#
    open('cmcl.json', 'w').write('''{
"exitWithMinecraft": false,
"javaPath": "jdk-21//bin//java.exe",
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
    system('cls')

#检测是否需要更新#
def check():
    global nV
    global nOF
    h = {'User-Agent':'Mozilla/5.0'}
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
        first = True #标记第一次启动（没有已安装版本）#

    #第一次启动,OF没更新#
    if first and noOF:
        nV = vL[1] #下载版本改为上一个版本#
        nOF = get('https://download.mcbbs.net/optifine/'+nV,headers=h).json() #重新获取OF版本#
        nOF = nOF[0]['type']+'_'+nOF[0]['patch']
        return True

    #第一次启动,有OF#
    elif first and not noOF:
        return True

    #不是第一次启动,OF没更新#
    elif not first and noOF:
        nV = oV #指定已有版本#
        nOF = oOF
        return False #不更新，等待OF更新新版本#

    #常规判断#
    if oV != nV or oOF != nOF:
        return True

#下载新版本#
if check():
    try:
        #删除旧版本（不影响存档）#
        rmtree('.minecraft/versions')
        mkdir('.minecraft/versions')
    except:pass
    #下载#
    system('jdk-21\\bin\\java.exe -jar cmcl.jar install %s --optifine %s -n %s-%s' %(nV,nOF,nV,nOF))

    if not path.exists('.minecraft/saves'): #判断第一次下载#
        open('.minecraft/options.txt', 'w').write('lang:'+lang) #自动修改游戏语言#
        open('.minecraft/optionsof.txt', 'w').write('''ofSmoothFps:true
ofRenderRegions:true
ofSmartAnimations:true
ofFastMath:true
ofFastRender:true
ofChunkUpdatesDynamic:true''') #开启优化设置#
    system('cls')

try:
    #自动分配内存#
    m = loads(open('cmcl.json', 'r').read())
    m["maxMemory"] = virtual_memory().available//1153433 #获取可用内存并修改cmcl.json#
    open('cmcl.json', 'w').write(str(m))
except:pass

#我的世界，启动！#
system('"jdk-21\\bin\\java.exe" -jar cmcl.jar %s-%s' %(nV,nOF))
