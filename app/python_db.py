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
    日记配置
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
        self.db = MySQLdb.connect(    #数据库连接
            host   = host,
            port   = port,
            user   = user,
            passwd = passwd,
            db     = db,
            charset= charset,
        )

    def getExample(self):
        return self.db.cursor() #实例化数据库连接
  
    def getDb(self):
        return self.db  

#数据库链接
class LinkMysql():

    def __init__(self):
        self.model = Db(db['host'], db['port'], db['user'], db['passwd'], db['db']);
        self.cur = self.model.getExample() #实例化链接
        self.log_setting = LoggingSetting() #实例化日记配置 
        self.db  = self.model.getDb()

    #添加数据
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
            self.rc = self.__param(sql)   #提交sql
            self.db.commit()              #提交数据库插入

        except Exception as e:
            print e
            self.__log(sql,2)

        return self.rc
  
  
    #删除数据
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
  
    #更新数据
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
  
    #查询数据多条数据
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
  
    #查询单挑语句
    def _find(self, table, field, where):

        try:

            sql = 'select %s from `%s` where %s'% (','.join(field), table, ' and '.join([' %s = %s '% (a,b) for a,b in where.iteritems()]))
            self.__param(sql)
            self.rc = self.__findone()

        except Exception as e:
            print e
            self.__log(sql,2)

        return self.rc 	


    #参数  
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
  
    #返回结果  
    def __findone(self):
 
        return self.cur.fetchone()

    #返回全部结果
    def __selectAll(self):
        return self.cur.fetchall()

    #摧毁	
    def __del__(self):
        self.cur.close()	


  

