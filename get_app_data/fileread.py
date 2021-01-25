import string

class FileRead():

    def __init__(self, fname):

        self.items = self.read_dict(fname)

    def read_dict(self,fpath):

        file_open = open(fpath)
        items = [i.strip() for i in file_open]
        file_open.close()
        return items

