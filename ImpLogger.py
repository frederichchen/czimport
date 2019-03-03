class ImpLogger:
    """ ImpLogger 类，记录日志

    Attributes:
        fh           日志文件的句柄
    """

    def __init__(self, logpath):
        try:
            self.fh = open(logpath, 'w')
        except IOError:
            print("无法打开日志文件！\n")

    def write_log(self, msg):
        self.fh.write(msg + '\n')

    def close_log(self):
        self.fh.close()
