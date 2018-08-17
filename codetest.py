
class Comparation (object):
    def __init__(self):
        self._ov = [1]
        self._ov[0] = "1"
        self.bool = False

    def __getitem__(self,k):
        return self.bool

    def __setitem__(self, k, new_val):
        self._nv = new_val
        if not self._ov[0] == self._nv :
            print("changed from ",self._ov[0],"to",self._nv)
            self._ov[0] = self._nv
            self.bool = False
            return
        self.bool = True


c = Comparation()
# c[0] = "ss"
for i in range(6):
    if i >= 2 :
        c[0] = "data2"
        print(c[0])

        

