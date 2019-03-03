import re
import sys
import cx_Oracle


class DataExtractor:
    """ DataExtractor 类，执行脚本提取数据

    Attributes:
        host         字符串类型，Oracle 主机名称或IP地址
        sid          字符串类型，Oracle 的 SID
        stmts        列表类型，待执行的语句
    """

    def __init__(self, host, sid, sqlpath):
        self.host = host
        self.sid = sid
        with open(sqlpath, 'r') as f:
            contents = f.read()
        # 将语句按分号分隔开，并替换掉多余的白空格
        self.stmts = [re.sub(r'^\s+', '', re.sub(r'\s+', ' ', x)) for x in
                      contents.split(';') if not re.match(r'^\s+$', x)]

    def extract_data(self, user, district_code, district_name, year):
        """ 执行提数脚本，提取数据

        Args:
            user          数据要提取到的用户名
            district_code 行政区划代码
            district_name 行政区划名称
            year          数据年度

        Raises:
            cx_Oracle.DatabaseError    Oracle 数据库操作异常
        """

        sql = ''
        try:
            conn = cx_Oracle.connect(user, "1234", self.host + "/" + self.sid)
            cursor = conn.cursor()
            # 让数据库不区分大小写
            cursor.execute('ALTER SESSION SET NLS_COMP=ANSI')
            cursor.execute('ALTER SESSION SET NLS_SORT=BINARY_CI')
            for stmt in self.stmts:
                # 判断取数脚本是否有 --insert ，有就插入，否则就仅仅执行
                if stmt == '':
                    continue
                res = re.search(r'-{2,}\s*insert (\S+) select (.+)',
                                stmt, re.IGNORECASE)
                if res:
                    inames = res.group(1).split('.')
                    # 判断表是否存在，如果存在就用 insert into ，否则就 create table
                    cursor.execute("select * from all_tables where owner='%s' and table_name='%s'" %
                                   (inames[0], inames[1]))
                    table_exists = cursor.fetchall()
                    if len(table_exists) == 0:
                        sql = "create table %s as select '%s' DISTRICT_CODE, '%s' DISTRICT_NAME, '%s' YEAR, %s" % (
                            res.group(1), district_code, district_name, year, res.group(2))
                        cursor.execute(sql)
                        cursor.execute(
                            'alter table %s modify DISTRICT_NAME VARCHAR2(100)' % res.group(1))
                    else:
                        sql = "insert into %s select '%s' DISTRICT_CODE, '%s' DISTRICT_NAME, '%s' YEAR, %s" % (
                            res.group(1), district_code, district_name, year, res.group(2))
                        cursor.execute(sql)
                        conn.commit()
                else:
                    cursor.execute(stmt)
            cursor.close()
            conn.close()
        except cx_Oracle.DatabaseError as e:
            print("执行 %s 语句失败！\n" % sql)
            print(e.args.context)
            sys.exit(1)
