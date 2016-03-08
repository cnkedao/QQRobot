#-*- coding:utf-8 -*-
import sys
import json
import logging
import traceback
import urllib
import urllib2
import multiprocessing
from urllib import unquote
import thread, ConfigParser
import datetime

logger = logging.getLogger("GATEWAY")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("debug.log")  
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s') 
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def echo(request,data):
    request.ret("OK")
    nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sdata = {} 
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.read("1.cfg")
    asksign= config.options("asksign")
    keywords = config.items("keywords")  
    status=0
    qqmess=config.get("global","qqmess")
    qqtail=config.get("global","qqtail")
    qqtail = qqtail+" "+nowtime
    for (key, value) in config.items("keyvalue"):  
        sdata[key] = value 
    t =data['data']
    print t
    s=json.loads(t)
    content = s['content']
    print content
    print s['group']
    gid=s['group_id']
    print gid
    
    if s['group'] == 'TrafficServer' or s['group'] == 'StaTeam' :
        print "team yes"
        for ask in asksign:
            print ask
            if ask in content:
                print "ask in content"
                print keywords
                for mykeyword in keywords:
                    print mykeyword
                    for key in mykeyword[1].split(','):
                        print "key:"+key
                        #print "key: "+key
                        #for key in keys:
                        if key in content:
                            status=1
                            print key
                            print "qqmess:"+qqmess
                            print sdata
                            print sdata[mykeyword[0]]
                            qqmess=qqmess+sdata[mykeyword[0]]
                            
                        else:
                            print "key not in content"
                break
            else:
                print "ask not in content"
        if status:
            print "status-------"
            todata=urllib.urlencode({'gid':gid,'content':qqmess+qqtail})
            url="http://127.0.0.1:5000/openqq/send_group_message"
            req = urllib2.Request(url=url,data=todata)
            urllib2.urlopen(req)
        else:
            print "status no"
    else:
        print "no"
    
class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
            try:
                method = getattr(cls._instance, "single_init")
                method()
            except Exception,e:
                logger.debug("Singleton "+e)
        return cls._instance

class gateway(Singleton):

    def single_init(self):
        logger.debug('gateway init')

    def test(self, request, response_head):
        data = request.form
        
        thread.start_new_thread(echo, (request,data))
