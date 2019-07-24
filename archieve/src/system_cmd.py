# -*- coding: utf-8 -*-
import datetime

def systemEcho(content):
    ''' system information print to screen'''
    print(content)
    systemLog(content)

def systemError(content):
    ''' exit program when somewhere errors'''
    content = '**ERROR** : ' + content
    print(content)
    print('Program Exits.')
    exit(0)

def systemLog(content):
    ''' output information into log file'''
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    out_str = now_time + '---' + content + '\n'
    with open('./system.log', 'a') as obj:
        obj.write(out_str)
