from os import path,remove,mkdir,listdir,system,chdir,popen
from shutil import rmtree,unpack_archive
from locale import getdefaultlocale
from psutil import virtual_memory
from subprocess import getoutput
from random import randint
from wget import download
from requests import get
from json import loads

h = {'User-Agent':'Mozilla/5.0'}

#获取系统语言#
lang,_ = getdefaultlocale()
lang = lang.lower()
system('cls')

#修改运行目录#
try:
    chdir('./DCML')
except:pass

#检查已安装的Java版本#
try:
    jv = getoutput('java -version')
    jv = jv.split('"')[1]
    jv = jv.split('.')[0]
    jv = int(jv)
except:
    jv = 0

#设置cmcl和java路径#
if jv >= 16:
    cmcl = 'cmcl.exe '
    java = ''
else:
    cmcl = 'jdk-21\\bin\\java.exe -jar cmcl.jar '
    java = '"javaPath": "jdk-21//bin//java.exe",'

#获取现有的游戏版本和OF#
oV = ''
oOF = ''
try:
    old = listdir('.minecraft/versions')[-1] #读取versions里的最后一个文件名#
    old = old.split('-') #通过“-”区分游戏版本和OF#
    oV = old[0]
    oOF = old[1]
except: #没有现有版本（第一次启动）#
    #创建DCML文件夹#
    mkdir('DCML')
    #修改运行目录#
    chdir('./DCML')

    #生成玩家名#
    name = 'Player'+str(randint(1000,9999))
    if lang == 'zh_cn':
        print('欢迎使用DCML-大聪明启动器！\n你的游戏名是'+name)
    else:
        print('Welcome to use DCML!\nYour player name is '+name)

    try:
        if jv >= 16:
            #下载cmcl.exe#
            download('https://gitee.com/MrShiehX/console-minecraft-launcher/releases/download/2.2.1/cmcl.exe',bar=None)
            system('cls')
        else:
            #下载cmcl.jar#
            download('https://gitee.com/MrShiehX/console-minecraft-launcher/releases/download/2.2.1/cmcl.jar',bar=None)
            system('cls')

            #下载Java并解压#
            download('https://d6.injdk.cn/openjdk/openjdk/21/openjdk-21_windows-x64_bin.zip')
            unpack_archive('openjdk-21_windows-x64_bin.zip')
            remove('openjdk-21_windows-x64_bin.zip')
            system('cls')
    except:
        #无网络时报错#
        if lang == 'zh_cn':
            print('下载出错，请检测网络或稍后重试')
        else:
            print('Download error, please check the network or try again later')
        while True:pass

    #创建cmcl.json#
    open('cmcl.json', 'w').write('''{
"exitWithMinecraft": false,
%s
"downloadSource": 2,
"checkAccountBeforeStart": false,
"accounts": [{
"playerName": "%s",
"loginMethod": 0,
"selected": true
}],
"printStartupInfo": false,
"maxMemory": 4096
}''' %(java,name))

#获取游戏正式版列表#
vL = []
nV = get('https://download.mcbbs.net/mc/game/version_manifest.json',headers=h).json()
for i in range(len(nV["versions"])):
    if nV["versions"][i]["type"] == "release": #筛选类型是正式版的版本#
        vL.append(nV["versions"][i]["id"]) #版本号加入列表#

#寻找有OF的最新游戏版本#
for nV in vL:
    nOF = get('https://download.mcbbs.net/optifine/'+nV,headers=h).json() #根据基准版本获取OF列表#
    try:
        nOF = nOF[0]['type']+'_'+nOF[0]['patch'] #截取版本号#
        break #成功立即跳出#
    except:pass #内容为空，继续寻找#

if oV != nV or oOF != nOF: #当前版本与最新版本不同时#
    #更新#
    try:
        #删除旧版本（不影响存档）#
        rmtree('.minecraft/versions')
        mkdir('.minecraft/versions')
    except:pass

    #下载#
    system(cmcl+' install %s --optifine %s -n %s-%s' %(nV,nOF,nV,nOF))

    if not path.exists('.minecraft/saves'): #判断第一次下载#
        open('.minecraft/options.txt', 'w').write('lang:'+lang) #自动修改游戏语言#
        open('.minecraft/optionsof.txt', 'w').write('''ofSmoothFps:true
ofRenderRegions:true
ofSmartAnimations:true
ofFastMath:true
ofFastRender:true
ofChunkUpdatesDynamic:true''') #开启优化设置#
    system('cls')

#自动分配内存#
try:
    m = loads(open('cmcl.json', 'r').read())
    m["maxMemory"] = virtual_memory().available//1153430 #获取可用内存并修改cmcl.json#
    open('cmcl.json', 'w').write(str(m))
except:pass

#我的世界，启动！#
system(cmcl+'%s-%s' %(nV,nOF))
