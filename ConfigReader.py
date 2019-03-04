import configparser
import sys
import os


class ConfigReader:
    """ ConfigReader 类，读取 config.ini 文件中的配置

    配置选项有：
    [oracle] section 中主要指定 Oracle 相关参数，选项如下：
    host         主机名或IP地址
    sid          Oracle 服务的 SID
    syspass      Oracle system用户的密码
    tables       需要恢复的表名，表名间用逗号分隔，如果为空就恢复所有的表
    improg       恢复的命令，可以是 imp 或 impdp

    [dmps] section 中主要指定待恢复文件相关参数，选项如下：
    dir          待恢复文件所在目录
    files        待恢复的文件路径，文件路径间用逗号分隔，如果该选项与 dir 选项都有值，则忽略 dir 选项
    suffix       文件后缀，可以为 dmp ，如果是压缩文件，也可以为 7z、rar等
    params       导入 dmp 文件所需的额外参数，比如 grants=no constraints=no
    decompressor 解压缩程序的路径，比如 C:/Program Files/7-Zip/7z.exe
    decompdir    解压缩文件的目录，如果需要解压缩，则需要指定该选项

    [operation] section 中主要指定dmp文件恢复后的一些操作，选项如下：
    log          日志文件路径
    deluser      数据提取完成后是否 drop user，如果为 yes 就删除，否则不删除
    districts    行政区划代码所在的 csv 文件路径
    extractor    提数脚本的路径
    modifier     修改表结构脚本的路径
    """

    def __init__(self, conf_path):
        conf = configparser.ConfigParser()
        try:
            conf.read(conf_path)
            self.host = conf.get('oracle', 'host')
            self.sid = conf.get('oracle', 'sid')
            self.syspass = conf.get('oracle', 'syspass')
            self.tables = conf.get('oracle', 'tables')     # 对应Oracle的tables选项
            self.improg = conf.get('oracle', 'improg')   # 使用imp还是impdp导入
            self.files = conf.get('dmps', 'files')         # files用来指定文件
            # dir用来指定文件所在目录，与files只能有一个
            self.dir = conf.get('dmps', 'dir')
            self.suffix = conf.get('dmps', 'suffix')       # 文件后缀，可以使dmp、7z等
            self.params = conf.get('dmps', 'params')   # 其他导入参数，比如 REMAP_SCHEMA
            self.decompressor = conf.get('dmps', 'decompressor')  # 解压缩程序路径
            self.decompdir = conf.get('dmps', 'decompdir')        # 解压到哪个目录
            self.log = conf.get('operations', 'log')
            self.deluser = conf.get('operations', 'deluser')      # 提取完后是否删除用户
            self.districts = conf.get('operations', 'districts')  # 行政区划代码的文件
            self.extractor = conf.get('operations', 'extractor')  # 提数脚本
            self.modifier = conf.get('operations', 'modifier')    # 修改表结构脚本
        except configparser.Error:
            print("配置文件有误，请检查路径是否正确，且必填字段是否存在！\n")
            sys.exit(1)
        if self.host == '':
            self.host = 'localhost'
        if self.sid == '':
            self.sid = 'orcl'
        if self.syspass == '' or self.improg == '':
            print("syspass、tablespace、improgs这三个选项的值不能为空！\n")
            sys.exit(1)
        if self.files == '' and self.dir == '':
            print("未指定待导入的文件或所在的目录！\n")
            sys.exit(1)
        if self.suffix == '':
            self.suffix == 'dmp'
        if self.suffix == 'dmp':
            self.decompressor = ''
            self.decompdir = ''
        else:
            if self.decompressor == '' or self.decompdir == '':
                print('压缩文件请指定decompressor选项中的解压缩程序路径以及decompdir选项中的解压缩路径！\n')
                sys.exit(1)
            if not os.path.isfile(self.decompressor):
                print('未找到解压缩软件，请查看decompressor路径是否正确！\n')
                sys.exit(1)
        if self.extractor != '' and not os.path.isfile(self.extractor):
            print('请检查提数脚本的路径是否正确！\n')
            sys.exit(1)
        if self.improg != 'imp' and self.improg != 'impdp':
            print('请正确指定improgs参数，只能为imp或者impdp！\n')
            sys.exit(1)
        if not os.path.isfile(self.districts):
            print('请正确指定districts参数，以读取行政区划代码对应表！\n')
            sys.exit(1)
