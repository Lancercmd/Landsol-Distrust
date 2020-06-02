from nonebot import on_command, CommandSession
from os import path

import datetime, nonebot, os, random

try:
    import ujson as json
except ImportError:
    import json

bot = nonebot.get_bot()
SUPERUSERS = bot.config.SUPERUSERS[0]  # 您可以将此处改为列表，并对相关代码进行更改

MONTH_NAME = ('睦月', '如月', '弥生','卯月', '皐月', '水無月','文月', '葉月', '長月','神無月', '霜月', '師走')

DATE_NAME = ('初一', '初二', '初三', '初四', '初五', '初六', '初七', '初八', '初九', '初十',
             '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十',
             '廿一', '廿二', '廿三', '廿四', '廿五', '廿六', '廿七', '廿八', '廿九', '三十',
             '卅一')

NUM_NAME = ('〇〇', '〇一', '〇二', '〇三', '〇四', '〇五', '〇六', '〇七', '〇八', '〇九',
            '一〇', '一一', '一二', '一三', '一四', '一五', '一六', '一七', '一八', '一九', 
            '二〇', '二一', '二二', '二三', '二四', '二五', '二六', '二七', '二八', '二九', 
            '三〇', '三一', '三二', '三三', '三四', '三五', '三六', '三七', '三八', '三九', 
            '四〇', '四一', '四二', '四三', '四四', '四五', '四六', '四七', '四八', '四九', 
            '五〇', '五一', '五二', '五三', '五四', '五五', '五六', '五七', '五八', '五九',
            '六〇', '六一', '六二', '六三', '六四', '六五', '六六', '六七', '六八', '六九', 
            '七〇', '七一', '七二', '七三', '七四', '七五', '七六', '七七', '七八', '七九', 
            '八〇', '八一', '八二', '八三', '八四', '八五', '八六', '八七', '八八', '八九', 
            '九〇', '九一', '九二', '九三', '九四', '九五', '九六', '九七', '九八', '九九')

CACHE = ''
DATA = {'CN':{},'JP':{},'KR':{},'QQ':{},'TW':{}}
FLAG = False

DISTRUST = path.join(os.path.dirname(__file__), 'distrust') + '.json'  # 兰德索尔失信人员名单
if not path.exists(DISTRUST):
    with open(DISTRUST, 'w', encoding='utf-8') as file:
        json.dump(DATA, file, ensure_ascii=False, indent=4)

FORMAT = '接口错误~'

A_FORMAT = '需要按格式提交~\n※ 如 /ld -a jp 305863117 此处应有100字图文丢人事迹'

F_FORMAT = '需要按格式查询~\n※ 如 /ld -f jp 305863117'

GROUP_ONLY = '该功能仅限群聊内使用~'

NOT_FOUND = '没有找到这条记录~'


@on_command('landsol_distrust', aliases=('/ld'), only_to_me=False)  # 兰德索尔失信人员名单
async def landsol_distrust(session:CommandSession):
    global CACHE, DATA, FLAG
    message = ''
    uid = str(session.event.user_id)
    if session.event.detail_type != 'group':
        await session.finish(GROUP_ONLY)
    if session.current_arg != 'y':        
        INPUT = session.current_arg
        CACHE = INPUT
        if INPUT == '':
            await session.finish(FORMAT)        
        L_INPUT = INPUT.split(' ', 3)
        if L_INPUT[0] == '-a':
            try:
                if L_INPUT[1] == 'CN' or L_INPUT[1] == 'Cn' or L_INPUT[1] == 'cN' or L_INPUT[1] == 'cn':
                    sid = 'CN'
                if L_INPUT[1] == 'JP' or L_INPUT[1] == 'Jp' or L_INPUT[1] == 'jP' or L_INPUT[1] == 'jp':
                    sid = 'JP'
                if L_INPUT[1] == 'KR' or L_INPUT[1] == 'Kr' or L_INPUT[1] == 'kR' or L_INPUT[1] == 'kr':
                    sid = 'KR'
                if L_INPUT[1] == 'QQ' or L_INPUT[1] == 'Qq' or L_INPUT[1] == 'qQ' or L_INPUT[1] == 'qq':
                    sid = 'QQ'
                if L_INPUT[1] == 'TW' or L_INPUT[1] == 'Tw' or L_INPUT[1] == 'tW' or L_INPUT[1] == 'tw':
                    sid = 'TW'
                id, notes = L_INPUT[2], L_INPUT[3]
            except IndexError:
                if FLAG == True:
                    FLAG = False
                    return
                await session.finish(A_FORMAT)    
            with open(DISTRUST, 'r', encoding='utf-8') as file:
                DATA = json.load(file)
            if id in DATA[sid]:
                FLAG = True
                confirm = session.get('message', prompt=f'ID {id} 已存在于兰德索尔失信人员名单~\n{DATA[sid][id]}\n※ 回复 y 更新此 ID 的不良行为~\n※ 回复其他内容取消操作~')
        if L_INPUT[0] == '-f':
            try:
                if L_INPUT[1] == 'CN' or L_INPUT[1] == 'Cn' or L_INPUT[1] == 'cN' or L_INPUT[1] == 'cn':
                    sid = 'CN'
                if L_INPUT[1] == 'JP' or L_INPUT[1] == 'Jp' or L_INPUT[1] == 'jP' or L_INPUT[1] == 'jp':
                    sid = 'JP'
                if L_INPUT[1] == 'KR' or L_INPUT[1] == 'Kr' or L_INPUT[1] == 'kR' or L_INPUT[1] == 'kr':
                    sid = 'KR'
                if L_INPUT[1] == 'QQ' or L_INPUT[1] == 'Qq' or L_INPUT[1] == 'qQ' or L_INPUT[1] == 'qq':
                    sid = 'QQ'
                if L_INPUT[1] == 'TW' or L_INPUT[1] == 'Tw' or L_INPUT[1] == 'tW' or L_INPUT[1] == 'tw':
                    sid = 'TW'
                id = L_INPUT[2]
            except IndexError:
                await session.finish(F_FORMAT)    
            with open(DISTRUST, 'r', encoding='utf-8') as file:
                DATA = json.load(file)            
            if id in DATA[sid]:
                await session.finish(DATA[sid][id])
            else:
                await session.finish(f'没有找到 ID {id} 的记录~')
    INPUT = CACHE        
    L_INPUT = INPUT.split(' ', 3)
    if L_INPUT[1] == 'CN' or L_INPUT[1] == 'Cn' or L_INPUT[1] == 'cN' or L_INPUT[1] == 'cn':
        sid = 'CN'
    if L_INPUT[1] == 'JP' or L_INPUT[1] == 'Jp' or L_INPUT[1] == 'jP' or L_INPUT[1] == 'jp':
        sid = 'JP'
    if L_INPUT[1] == 'KR' or L_INPUT[1] == 'Kr' or L_INPUT[1] == 'kR' or L_INPUT[1] == 'kr':
        sid = 'KR'
    if L_INPUT[1] == 'QQ' or L_INPUT[1] == 'Qq' or L_INPUT[1] == 'qQ' or L_INPUT[1] == 'qq':
        sid = 'QQ'
    if L_INPUT[1] == 'TW' or L_INPUT[1] == 'Tw' or L_INPUT[1] == 'tW' or L_INPUT[1] == 'tw':
        sid = 'TW'
    id, notes = L_INPUT[2], L_INPUT[3]        
    year = int(datetime.datetime.now().strftime('%Y'))  # 未使用，可酌情删除
    month = int(datetime.datetime.now().strftime('%m'))-1
    day = int(datetime.datetime.now().strftime('%d'))-1
    hour = int(datetime.datetime.now().strftime('%H'))
    minute = int(datetime.datetime.now().strftime('%M'))
    time = f'{MONTH_NAME[month]}{DATE_NAME[day]} · {NUM_NAME[hour]}{NUM_NAME[minute]}'
    DATA[sid][id] = f'(待审核){time}\n{notes}'
    if sid == 'QQ':
        message += f'{time}\n(待审核)\n失信人员 QQ {id}\n上报事由 {notes}'
    else:
        message += f'{time}\n(待审核)\n失信人员 ID {id}\n区服 {sid}\n上报事由 {notes}'
    with open(DISTRUST, 'w', encoding='utf-8') as file:
        json.dump(DATA, file, ensure_ascii=False, indent=4)
    info = await bot.get_stranger_info(user_id=uid)  # 获取个人资料
    username = info['nickname']  # 获取昵称
    message += f'\n※ 申诉请前往 https://github.com/Lancercmd/Landsol-Distrust 或使用优妮来杯咖啡'  # 来杯咖啡，联动 IceCirno / HoshinoBot https://github.com/Ice-Cirno/HoshinoBot
    if sid == 'QQ':
        await session.bot.send_private_msg(user_id = SUPERUSERS, message = f'有新的失信人员进入审核~\n(待审核){time}\n失信人员 QQ {id}\n上报事由 {notes}\n※ 本条记录由 {username}({uid}) 上报~')
    else:
        await session.bot.send_private_msg(user_id = SUPERUSERS, message = f'有新的失信人员进入审核~\n(待审核){time}\n失信人员 ID {id}\n区服 {sid}\n上报事由 {notes}\n※ 本条记录由 {username}({uid}) 上报~')  # 向主人发送私聊记录，仅向主人展示上报者的身份以保密
    #####################################################
    #============此处可以向审核们推送message============#
    #####################################################
    await session.finish(f'ID {id} 已进入公开审核~\n※ 待审核通过即会正式进入兰德索尔失信人员名单~\n※ 恶意上报将不会被收入，同时您将会进入兰德索尔失信人员名单！')
