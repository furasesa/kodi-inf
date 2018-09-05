class Comparation (object):
    def __init__(self):
        self._ov = [1]
        self._ov[0] = None
        self.bool = False
        
    def __getitem__(self,k):
        return self.bool

    def __setitem__(self, k, new_val):
        self._nv = new_val
        if not self._ov[0] == self._nv :
            print("changed from ",self._ov[0],"to",self._nv)
            # try:
            #     # if arduino_connected:
            #     arduino.write(self._nv.encode())
            # except:
            #     logging.error("error comparation serial")
            self._ov[0] = self._nv
            self.bool = False
            return
        self.bool = True
