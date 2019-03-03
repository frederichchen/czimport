import sys
import os


class DataModifier:
    """ DataModifier 类，执行脚本修改表结构

    Attributes:
        sid          字符串类型，Oracle 的 SID
        syspass      字符串类型，Oracle system 用户的密码
    """

    def __init__(self, sid, syspass):
        self.sid = sid
        self.syspass = syspass

    def modify_data(self, sqlpath):
        if os.system("sqlplus system/%s@%s as sysdba @%s" % (self.syspass, self.sid, sqlpath)) != 0:
            print("表结构调整语句执行出错！\n")
            sys.exit(1)
