# 财政数据批量导入提取程序使用指南

## 简介

czimport 是用 Python 开发的批量导入财政大平台系统 dmp 文件，执行给定查询并将结果提取到给定用户下的数据表的程序。

## 环境要求

该程序是在 Windows 环境下开发测试的，没有尝试过在 Linux 环境下的情况。

程序运行须安装的软件：

    1. Oracle 数据库
    2. python3 解释器
    3. cx_Oracle 库，安装命令： pip install cx_oracle
    4. 7-Zip 解压缩软件（如果文件是压缩格式的话）

## 使用方法

### 配置参数

使用时须修改配置文件 config.ini ，指定各项参数，参数的意义如下：

    [oracle] section 中主要指定 Oracle 相关参数，选项如下：
    host         主机名或IP地址，默认是 localhost
    sid          Oracle 服务的 SID，默认是 orcl
    syspass      [必填]Oracle system用户的密码
    tables       需要恢复的表名，表名间用逗号分隔，如果为空就恢复所有的表
    improg       [必填]恢复的命令，可以是 imp 或 impdp

    [dmps] section 中主要指定待恢复文件相关参数，选项如下：
    dir          待恢复文件所在目录
    files        待恢复的文件路径，文件路径间用逗号分隔，如果该选项与 dir 选项都有值，则忽略 dir 选项
    suffix       文件后缀，默认为 dmp ，如果是压缩文件，也可以为 7z、rar等
    params       导入 dmp 文件所需的额外参数，比如 grants=no constraints=no
    decompressor 解压缩程序的路径，比如 C:\Program Files\7-Zip\7z.exe
    decompdir    解压缩文件的目录，如果需要解压缩，则需要指定该选项

    [operation] section 中主要指定dmp文件恢复后的一些操作，选项如下：
    log          [必填]日志文件路径
    deluser      数据提取完成后是否 drop user，如果为 yes 就删除，否则不删除
    districts    [必填]行政区划代码所在的 csv 文件路径
    extractor    提数脚本的路径
    modifier     修改表结构脚本的路径

### 行政区划代码格式

行政区划代码必须为 **csv** 格式的文件，格式如下：

    用户名,行政区划代码,年度,行政区划名称

### 提数脚本的结构

提数脚本必须为规范的 SQL 脚本，多个语句间 **必须用分号分隔** ！！需要提取数据的语句上面必须要加入类似 **--insert 用户名.表名** 的注释，例如：

    --insert TEST.TABLE1
    SELECT F1, F2, F3
    FROM T1;

    --insert SCCZTEST.TABLE2
    SELECT F1, F2, F3, F4 FROM T2;

### 执行程序

配置好各项参数后，执行如下命令就可以开始批量导入提取：

    python3 start.py
