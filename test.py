#coding=utf8
import itchat
import mysql.connector as db

dbconfig = {  'user':'dan',
              'password':'123456',
              'host':'127.0.0.1',
              'database':'wchat',
              'raise_on_warnings':True}

dbc = db.connect(**dbconfig)




def get_ChatroomInfo():
    ChatroomGroup = {}
    roomlist = itchat.get_chatrooms(update=True)
    if len(roomlist):
        for x in roomlist:
            ChatroomGroup.update({x['UserName']: {'NickName': x['NickName'], 'MemberCount': x['MemberCount']}})
        return ChatroomGroup
    else:
        return None


def search_ChatRoomInfo(Roomname=None):
    UserList = []
    if Roomname:
        ChatroomName = itchat.search_chatrooms(name=Roomname)
        if ChatroomName:
            UserName,NickName = ChatroomName[0]['UserName'],ChatroomName[0]['NickName']
            ChatroomInfo = {'RoomName':UserName, 'NickName': NickName}
            ChatroomNameMemberList = itchat.update_chatroom(UserName, detailedMember=True)
            if len(ChatroomNameMemberList):
                for x in ChatroomNameMemberList['MemberList']:
                    a = [('UserName', x['UserName']), ('NickName', x['NickName']), ('Province', x['Province']),
                          ('City', x['City']),('Gender', x['Sex'])]
                    UserList.append(a)
            ChatroomInfo.update({'MemberList':UserList})
            return ChatroomInfo
        else:return None
    else:return None

def query_roominfo(GroupName = None,Rowcount=False):
    Gid=NickName=GName = None
    if GroupName:
        #gname = GroupName
        cursor = dbc.cursor()
        query = ("select GroupID,NickName,GroupName from wchatgroup where GroupName = %(GroupName)s")
        cursor.execute(query,{'GroupName':GroupName})
        for a,b,c in cursor:
            Gid, NickName, GName = a,b,c
        cursor.close()
    if Rowcount:
        return cursor.rowcount
    else:
        return Gid,NickName,GName

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

def update_roomlist_info(Info=None):
    if not query_roominfo(GroupName=Info['RoomName'],Rowcount=True):
        cursor = dbc.cursor()
        exec_room = ("Insert into wchatgroup (NickName,GroupName) values (%(NickName)s,%(GroupName)s)")
        GroupInfo = {
            'NickName':Info['NickName'],
            'GroupName':Info['RoomName']
        }
        cursor.execute(exec_room, GroupInfo)
        # dbc.commit()
        # print('插入数据%s成功'%info['NickName'])

def update_Member_info(Info=None):
    if Info:
        for x in Info:
            if not query_memberinfo(MemberInfo=x,Rowcount=True):
                cursor = dbc.cursor()
                exec_room = ("Insert into wchatuser (uname,NickName,Gender,Province,City) values (%(UserName)s,%(NickName)s,%(Gender)s,%(Province)s,%(City)s)")
                #print(dict(x))
                cursor.execute(exec_room, dict(x))





#
# @itchat.msg_register(itchat.content.TEXT,isGroupChat=True)
# def print_content(msg):
#     # for x in msg:
#     #    print(x+' '+repr(msg[x]))
#     print(msg)
#
#     print(msg['ActualNickName'] + '  '+msg['Text'])
#     # print(msg['User']['NickName'])

itchat.auto_login(hotReload=True)
info = search_ChatRoomInfo(Roomname='芳满')
print(info)
update_Member_info(Info=info['MemberList'])
dbc.commit()

itchat.run()

dbc.close()
