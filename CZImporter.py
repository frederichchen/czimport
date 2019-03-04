import sys
import os
import glob
import csv
import time
from ConfigReader import *
from Decompressor7z import *
from DmpImporter import *
from DataExtractor import *
from DataModifier import *
from ImpLogger import *


class CZImporter:
    """ CZImporter 类，批量导入数据

    Attributes:
        conf         ConfigReader类型，包含配置参数信息
        files        列表类型，待导入的文件路径
        districts    字典类型，包含行政区划信息
        decompressor 解压缩程序
        importer     DmpImporter类型，执行单个dmp文件的导入
        extractor    DataExtractor类型，执行数据提取操作
        modifier     DataModifier类型，执行修改表结构操作
        logger       ImpLogger类型，记录日志
    """

    def __init__(self, conf_path=''):
        # 读取配置文件并将待导入文件加入列表
        if conf_path == '':
            conf_path = './config.ini'
        self.conf = ConfigReader(conf_path)
        self.files = []
        self.districts = {}
        # 将待导入的文件加入列表
        if self.conf.files != '':
            self.files = self.conf.files.split(',')
            for f in self.files:
                if not os.path.isfile(f):
                    print('%s 文件不存在！\n' % f)
                    sys.exit(1)
        else:
            if not os.path.isdir(self.conf.dir):
                print('dir选项指定的目录不存在！\n')
                sys.exit(1)
            self.files = glob.glob(
                self.conf.dir + '/**/*.' + self.conf.suffix, recursive=True)
        if len(self.files) == 0:
            print('没有找到待导入的文件，请查看配置是否正确！\n')
            sys.exit(1)

        # 文件后缀如果是dmp就不需要配置解压缩程序了
        if self.conf.suffix != 'dmp':
            self.decompressor = Decompressor7z(
                self.conf.decompressor, self.conf.decompdir)
        else:
            self.decompressor = None

        # 读取行政区划代码和年度数据
        with open(self.conf.districts) as f:
            reader = csv.reader(f)
            for row in reader:
                self.districts[row[0].upper()] = [row[1], row[2], row[3]]

        # 初始化导入组件
        self.importer = DmpImporter(self.conf.sid, self.conf.syspass,
                                    self.conf.tables, self.conf.params)
        # 初始化数据提取组件
        if self.conf.extractor != '':
            self.extractor = DataExtractor(self.conf.host,
                                           self.conf.sid, self.conf.extractor)
        else:
            self.extractor = None

        # 初始化表结构调整组件
        if self.conf.modifier != '':
            self.modifier = DataModifier(self.conf.sid, self.conf.syspass)
        else:
            self.modifier = None

        # 初始化日志记录组件
        self.logger = ImpLogger(self.conf.log)

    def create_user(self, filepath):
        """ 用户生成 cu.sql 和 du.sql 两个脚本，前者用于创建用户，后者用于删除用户

        Args:
            filepath    dmp文件路径，dmp文件需要用 用户名.dmp 的方式命名，比如 chenghua2018.dmp

        Returns:
            返回创建的用户名
        """

        uname = os.path.basename(filepath).split('.')[0].upper()
        with open('./cu.sql', 'w') as f:
            f.write('create user %s identified by 1234 account unlock;\n' % (
                uname))
            f.write('grant dba to %s with admin option;\n' % (uname))
            f.write('exit;\n')
        with open('./du.sql', 'w') as f:
            f.write('drop user %s cascade;\n' % (uname))
            f.write('exit;\n')
        if os.system("sqlplus system/%s@%s as sysdba @cu.sql" % (self.conf.syspass, self.conf.sid)) != 0:
            print("无法执行创建用户的语句！\n")
            sys.exit(1)
        return uname

    def del_user(self):
        """ 执行 du.sql 删除用户
        """

        if os.system("sqlplus system/%s@%s as sysdba @du.sql" % (self.conf.syspass, self.conf.sid)) != 0:
            print("无法执行删除用户的语句！\n")
            sys.exit(1)

    def batch_import(self):
        """ 执行批量导入工作

            步骤是：
            1. 从文件路径列表中取出一个文件
            2. 如果是压缩文件则解压缩
            3. 创建用户，然后对 dmp 文件进行导入
            4. 提取数据
            5. 如果是第一个导入的文件并存在 modifier ，则调用修改表结构
            6. 如果 deluser 选项是 yes，则删除用户
        """

        file_count = 0
        for f in self.files:
            self.logger.write_log("开始导入 %s ，时间是：%s。" % (
                f, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
            uname = self.create_user(f)
            if self.decompressor is None:
                self.importer.import_data(self.conf.improg, f, uname, False)
            else:
                self.decompressor.decompress(f)
                dmps = glob.glob(self.conf.decompdir + '/*.dmp')
                self.importer.import_data(self.conf.improg, dmps[0], uname)

            # 然后是提取数据
            if self.extractor is not None:
                extras = self.districts.get(uname, [uname, '0000', uname])
                self.extractor.extract_data(
                    uname, extras[0], extras[uname][2], extras[1])
            file_count = file_count + 1
            if self.modifier is not None and file_count == 1:
                self.modifier.modify_data(self.conf.modifier)

            if self.conf.deluser == 'yes':
                self.del_user()
            self.logger.write_log("文件 %s 处理完毕，时间是：%s。" % (
                f, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))

        self.logger.write_log("处理完毕，共处理%d个文件，时间是：%s。" % (
            file_count, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        self.logger.close_log()
