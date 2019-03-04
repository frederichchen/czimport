import os
import sys
from CZImporter import *


if len(sys.argv) > 2:
    print("参数个数不正确！\n")
    sys.exit(1)
if len(sys.argv) == 1:
    czimp = CZImporter()
else:
    if not os.path.isfile(sys.argv[1]):
        print("未找到指定的配置文件！\n")
        sys.exit(1)
    czimport = CZImporter(sys.argv[1])

czimp.batch_import()
