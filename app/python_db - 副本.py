#-*- coding: utf-8 -*-
#!/usr/bin/python
# Filename: python_db.py

import MySQLdb
import sys
import logging
from .config import *


class LoggingSetting():
    '''
    �ռ�����
    '''
    def __init__(self):
        log_url = log['log_url']
        logging.basicConfig(
            level   = logging.DEBUG,
            format  = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
            datefmt = '%a, %d %b %Y %H:%M:%S',
            filename= log_url,
            filemode= 'w'
        )





#���ݿ�����
class LinkMysql():

    def __init__(self, host, port, user, passwd, db, charset='utf8'):
        conn= MySQLdb.connect(
            host   = host,
            port   = port,
            user   = user,
            passwd = passwd,
            db     = db,
            charset= charset,
        )
        self.cur = conn.cursor() #ʵ�������ݿ�����
        self.log_setting = LoggingSetting() #ʵ�����ռ����� 


    #�������
    def add(self,table,**param):
        '''
        sql = 'insert into `table` (create) values(%s)'
        param = tuple('1')
        '''
        try:
            #sql = 'insert into `%s` (%s) values(%s)'% (param[0],param[1],param[2]) 
            k = []
            v = []
            for key,value in param.iteritems():
                k.append(key)
                v.append(value)

            sql = 'insert into `%s` (%s) values(%s)'%(table,','.join)
            self.rc = self.__param(sql)
            print self.rc
            self.__log(sql,param)
            self.cur.commit() #���ݿ����
        except Exception as e:
            self.__log(sql,param,2)

        return self.rc
  
  
    #ɾ������
    def delete(self,sql,param=()):
        '''
        sql = 'delete from `table` where id = %d'
        param = tuple('1')
        '''
        try:
            self.rc = self.__param(sql,param)
            self.__log(sql,param)
        except Exception as e:
            self.__log(sql,param,2)

        return self.rc 
  
    #��������  
    def update(self,sql,param=()):
        '''
        sql = 'update `table` set create = 1 where id = %d'
        param = tuple('1')
        '''
        try:
            self.rc = self.__param(sql,param)
            self.__log(sql,param)
        except Exception as e:
            self.__log(sql,param,2)

        return self.rc 
  
    #��ѯ���ݶ�������
    def select(self,sql,param = ()):
        '''
        sql = 'select * from `table` where id = %d'
        param = tuple('1')
        '''
        try:
            self.__param(sql,param)
            self.__log(sql,param)
            self.rc = self.__selectAll()
        except Exception as e:
            self.__log(sql,param,2)
        return self.rc 	
  
    #��ѯ�������
    def find(self,sql,param = ()):
        try:
            self.__param(sql,param)
            self.__log(sql,param)
            self.rc = self.__findone()
        except Exception as e:
            self.__log(sql,param,2)
        return self.rc 	


    #����  
    def __param(self,sql):
        if len(sql) == 0:
            print 'None sql'
            sys.exit()
        try:
            print sql
            rc = self.cur.execute(sql)
        except Exception as e:
            print e
        print rc
        return rc
  
    #log
    def __log(self,sql,param,level = 1):
        if int(level) == 1:
            logging.info('sql:'+str(sql)+';param:'+str(param))
        elif int(level) == 2:
            logging.warning('sql:'+str(sql)+';param:'+str(param))
  
    #���ؽ��  
    def __findone(self):
        return self.cur.fetchone()

    #����ȫ�����
    def __selectAll(self):
        return self.cur.fetchall()

    #�ݻ�	
    def __del__(self):
        self.cur.close()	






  

