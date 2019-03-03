import os


class Decompressor7z:
    """ Decompressor7z 类，解压缩文件

    Attributes:
        cmd          字符串类型，解压缩命令
    """

    def __init__(self, path, target):
        self.cmd = '"' + path + '" ' + ' -o' + target + ' x '

    def decompress(self, source):
        os.system(self.cmd + source)
