import os


class DmpImporter:
    """ DmpImporter 类，调用 imp 或 impdp 导入数据

    Attributes:
        sid          字符串类型，Oracle 的 SID
        syspass      字符串类型，Oracle system 用户的密码
        tables       字符串类型，需要导入的表名，表名间用逗号分隔
        params       字符串类型，导入时需要的额外参数
    """

    def __init__(self, sid, syspass, tables='', params='', delfile=True):
        self.sid = sid
        self.syspass = syspass
        self.tables = tables
        self.params = params

    def import_data(self, improg, filepath, user, delfile=True):
        """ 调用 imp 或 impdp 导入数据

        Args:
            improg        导入命令，可以是 imp 或 impdp
            filepath      dmp 文件路径
            user          导入数据的用户名
            delfile       导入完成后是否要删除dmp文件
        """

        cmd = ''
        if improg == 'imp':
            if self.tables == '':
                cmd = 'imp system/%s@%s file=%s fromuser=%s touser=%s %s' % (
                    self.syspass, self.sid, filepath, user, user, self.params)
            else:
                cmd = 'imp system/%s@%s file=%s fromuser=%s touser=%s tables=(%s) %s' % (
                    self.syspass, self.sid, filepath, user, user, self.tables, self.params)
        else:
            if self.tables == '':
                cmd = 'impdp %s/1234@%s dumpfile=%s %s' % (
                    user, self.sid, os.path.basename(filepath), self.params)
            else:
                cmd = 'impdp %s/1234@%s dumpfile=%s tables=(%s) %s' % (
                    user, self.sid, os.path.basename(filepath), self.tables, self.params)
        os.system(cmd)
        if delfile == True:
            os.remove(filepath)
