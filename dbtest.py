#coding=utf8
import itchat
import mysql.connector as db

dbconfig = {  'user':'dan',
              'password':'123456',
              'host':'127.0.0.1',
              'database':'wchat',
              'raise_on_warnings':True}

dbc = db.connect(**dbconfig)

def query_roominfo(GroupName = None,RowCount=False):
    Gid=NickName=GName = None
    if GroupName:
        #gname = GroupName
        cursor = dbc.cursor()
        query = ("select GroupID,NickName,GroupName from wchatgroup where GroupName = %(GroupName)s")
        cursor.execute(query,{'GroupName':GroupName})
        for a,b,c in cursor:
            Gid, NickName, GName = a,b,c
        cursor.close()
        if RowCount:
            return cursor.rowcount
    return Gid,NickName,GName

def update_roomlist_info(Info=None):
        cursor = dbc.cursor()
        exec_room = ("Insert into wchatgroup (NickName,GroupName) values (%(NickName)s,%(GroupName)s)")
        GroupInfo = {
            'NickName':'test',
            'GroupName':'@@dsjfklafppweoppfaeewkdskfl;akdsp'
        }
        cursor.execute(exec_room,GroupInfo)


def query_memberinfo(MemberInfo=None,Rowcount=False):
    uname=NickName=Gender=Province=City=None
    if MemberInfo:
            cursor = dbc.cursor()
            query = ("select uname,NickName,Gender,Province,City from wchatuser where uname = %(UserName)s")
            cursor.execute(query,dict(MemberInfo))
            for a,b,c,d,e in cursor:
                uname,NickName,Gender,Province,City=a,b,c,d,e
            if Rowcount:
                count = cursor.rowcount
                cursor.close()
                return count
            cursor.close()
    return uname,NickName,Gender,Province,City

def update_Member_info(Info=None):
    if Info:
        for x in Info:
            if not query_memberinfo(MemberInfo=x,Rowcount=True):
                cursor = dbc.cursor()
                exec_room = ("Insert into wchatuser (uname,NickName,Gender,Province,City) values (%(UserName)s,%(NickName)s,%(Gender)s,%(Province)s,%(City)s)")
                cursor.execute(exec_room, dict(x))



x = [[('UserName', '@b1773e69b59745cf735d6af9a155f3a45e1183c957b6d6a06cc316765e0c5eb6'), ('NickName', '林'), ('Gender',0),('Province', '广东'), ('City', '广州')]]
update_Member_info(x)
dbc.commit()
print("i am %(name)s, i am %(age)d years old" % {'name':'jeck','age':26})



