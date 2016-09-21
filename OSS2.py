# -*- coding: utf-8 -*-
"""
    wrapper of oss2.
"""
import oss2
from PwLogging import PwLogging
class OSS2(object):

    def __init__(self, accesskeyid, accesskeysecret, endpoint, bucket, logger=None):
        self.accessid = accesskeyid
        self.accesskey = accesskeysecret
        self.endpoint = endpoint
        self.bucketstring = bucket
        self.logger = logger
        self.connection()

    def connection(self):
        try:
            auth = oss2.Auth(self.accessid, self.accesskey)
            self.bucket = oss2.Bucket(auth, self.endpoint, self.bucketstring)
        except Exception, e:
            self.logger.error(e)

    def uploadFiles(self, remotepath, localpath, filenamelist):
        try:
            faildlist = []
            for file in filenamelist:
                result = self.bucket.put_object_from_file(remotepath + '/' + file, localpath + '/' + file)
                if int(result.status) != 200:
                    faildlist.append(file)
            return faildlist
        except Exception, e:
            self.logger.error(e)

    def deleteFiles(self, filename):
        try:
            seccesslist = []
            for object_info in oss2.ObjectIterator(self.bucket):
                if filename in object_info.key:
                    result = self.bucket.delete_object(object_info.key)
                    if not result.status and int(result.status) == 204:
                        seccesslist.append(object_info.key)
            return seccesslist
        except Exception, e:
            self.logger.error(e)

    def uploadfile(self, remotepath, localpath, filename):
        try:
            result = self.bucket.put_object_from_file(remotepath + '/' + filename, localpath + '/' + filename)
            if int(result.status) == 200:
                return True
            else:
                return False
        except Exception, e:
            self.logger.error(e)

    def deletefile(self, filename):
        try:
            for object_info in oss2.ObjectIterator(self.bucket):
                if filename in object_info.key:
                    result = self.bucket.delete_object(object_info.key)
                    if not result.status:
                        return None
                    elif int(result.status) == 204:
                        return True
                    else:
                        return False
        except Exception, e:
            self.logger.error(e)

if '__name__' == '__main__':
    LOGDIR = '/var/log'
    logger = PwLogging(dir=LOGDIR)
    logger.addRotatingFileHandler('test.log', level='debug', fmt='simple')

    oss = OSS2(accesskeyid = '', accesskeysecret = '', endpoint= 'http://oss-cn-hangzhou.aliyuncs.com', bucket= '',logger=logger)
    oss.uploadFiles()
    oss.deleteFiles()
