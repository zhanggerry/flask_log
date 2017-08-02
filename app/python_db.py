#-*- coding: utf-8 -*-
#!/usr/bin/python
# Filename: python_db.py

import MySQLdb
import sys
import logging
import types
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

class Db():
    def __init__(self, host, port, user, passwd, db, charset='utf8'):
        self.db = MySQLdb.connect(    #���ݿ�����
            host   = host,
            port   = port,
            user   = user,
            passwd = passwd,
            db     = db,
            charset= charset,
        )

    def getExample(self):
        return self.db.cursor() #ʵ�������ݿ�����
  
    def getDb(self):
        return self.db  

#���ݿ�����
class LinkMysql():

    def __init__(self):
        self.model = Db(db['host'], db['port'], db['user'], db['passwd'], db['db']);
        self.cur = self.model.getExample() #ʵ��������
        self.log_setting = LoggingSetting() #ʵ�����ռ����� 
        self.db  = self.model.getDb()

    #�������
    def _add(self, table, **param):
        '''
        sql = 'insert into `table` (create) values(%s)'
        param = tuple('1')
        '''
        try:
            k = []
            v = []
            for key,value in param.iteritems():
                k.append(key)
                v.append(value)
      
            sql = 'insert into `%s` (%s) values(%s)'%(table,','.join(['`%s`'% i for i in k]),','.join(['"%s"' % i for i in v]))
            self.rc = self.__param(sql)   #�ύsql
            self.db.commit()              #�ύ���ݿ����

        except Exception as e:
            print e
            self.__log(sql,2)

        return self.rc
  
  
    #ɾ������
    def _delete(self, table, **param):
        '''
        sql = 'delete from `table` where id = %d'
        param = tuple('1')
        '''
        try:
     
            sql = 'delete from `%s` where %s'% (table, ' and '.join([' %s = %s'% (a,b) for a,b in param.iteritems()]))
            self.rc = self.__param(sql)
   
        except Exception as e:
            print e
            self.__log(sql,2)

        return self.rc 
  
    #��������
    def _update(self, table, set, where):

        '''
        sql = 'update `table` set create = 1 where id = %d'
        param = tuple('1')
        set = {}
        where = {}
        '''

        try:
            if not type(set) == type(dict()):
                print 'set is not a Dict '
                sys.exit()

            if not type(where) == type(dict()):
                print 'where is not a Dict'
                sys.exit()

            sql = 'update `%s` set %s where %s'% (table, ' and '.join(['%s = %s'% (a,b) for a,b in set.iteritems()]), ' and '.join(['%s = %s'% (a,b) for a,b in where.iteritems()]))
            self.rc = self.__param(sql)

        except Exception as e:
            print e
            self.__log(sql,2)

        return self.rc 
  
    #��ѯ���ݶ�������
    def _select(self, table, field = '', where = {}, order = '',limit = ''):
        '''
        sql = 'select * from `table` where id = %d'
        param = tuple('1')
        '''
        try:
     
            if field:
                sql = 'select %s from `%s`'% (','.join(field), table)
            else :
                sql = 'select * from `%s`'% (table)

            if where :
                sql = sql + 'where %s'% (' and '.join([' %s = %s '% (a,b) for a,b in where.iteritems()]),)
            

            if order :
                sql = sql + ' order by %s'% order

            if limit:
            
                sql = sql + ' limit %s'% limit

            #sql = 'select %s from `%s` where %s'% (','.join(field), table, ' and '.join([' %s = %s '% (a,b) for a,b in where.iteritems()]))
            self.__param(sql)
            self.rc = self.__selectAll()
        except Exception as e:

            print e
            self.__log(sql,2)

        return self.rc 	
  
    #��ѯ�������
    def _find(self, table, field, where):

        try:

            sql = 'select %s from `%s` where %s'% (','.join(field), table, ' and '.join([' %s = %s '% (a,b) for a,b in where.iteritems()]))
            self.__param(sql)
            self.rc = self.__findone()

        except Exception as e:
            print e
            self.__log(sql,2)

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
    
        self.__log(sql)
        return rc
  
    #log
    def __log(self,sql,level = 1):
        if int(level) == 1:
            logging.info('sql:'+str(sql))
        elif int(level) == 2:
            logging.warning('sql:'+str(sql))
  
    #���ؽ��  
    def __findone(self):
 
        return self.cur.fetchone()

    #����ȫ�����
    def __selectAll(self):
        return self.cur.fetchall()

    #�ݻ�	
    def __del__(self):
        self.cur.close()	


  

