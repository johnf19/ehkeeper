# -*- coding : UTF-8 -*-
'''
author johnf19
EHViewer Download Files Keeper
Version 0.1.0beta

'''
print('\033[1;36;43mEHViewer Download Files Keeper\tVersion 0.1.0beta\033[0m')
import sqlite3
import os,re
import sys

exe = []
exec = []

def escape(shellist, n = 0):
    ngword = ['*', '?', '[', ']', '^', '!', '{', '}', '(', ')', '\'']
    #shellist = list(shell)
    tm = 1
    for i in ngword:
        if n == len(shellist):
            break
        elif shellist[n] == i:
            shellist.insert(n, "\'\\")
            shellist.insert(n+2, "\'")
            n += 3
            escape(shellist,n)
        elif tm < len(ngword):
            tm += 1
            continue
        else:
            n += 1
            escape(shellist,n)
    return ''.join(shellist)

def type_con(n):
    n = int(n)
    if n == 1:
        return 'MISC'
    elif n == 2:
        return 'DOUJINSHI'
    elif n == 4:
        return 'MANGA'
    elif n == 8:
        return 'Artist_CG'
    elif n == 16:
        return 'GAME_CG'
    elif n == 32:
        return 'IMAGE_SET'
    elif n == 64:
        return 'COSPLAY'
    elif n == 512:
        return 'WESTERN'
    else:
        return n

def gid_get(n):
    get_gid = re.compile(r'\d+')
    ggid = get_gid.match(n)
    return ggid.group()
    #print(gid)

mydb=sqlite3.connect("eh.db")
cursor=mydb.cursor()
cursor.execute("SELECT GID, CATEGORY FROM DOWNLOADS;")
Tables=cursor.fetchall()
#print(Tables)
#print(Tables[1][2])

def lookup(i):
    for n in range(len(Tables)):
        gid = gid_get(i)
        #print(gid)
        if int(gid) == int(Tables[n][0]):
            #print('yes')
            type = int(Tables[n][1])
            #print(gid,type,i)
            exe.append(i)
            exe.append(type)

def cmdmake(m, n):
    fn = escape(m)
    typ = type_con(n)
    command = 'mv \'%s\' \'%s\'/'% (fn, typ)
    exec.append(command)

path = sys.path[0]
dir = os.listdir(path)
#print(dir)
for folder in dir:
    try:
        lookup(folder)
    except:
        pass
#print(exe)
n = 0
while n <= 10:
    dir = type_con(2**n)
    shell = 'mkdir \'%s\'/'% (dir)
    #print(shell)
    os.system(shell)
    n += 1
n = 0
while n < len(exe):
    cmdmake(list(exe[n]), exe[n+1])
    n += 2

print(exec)
for n in exec:
    os.system(n)
