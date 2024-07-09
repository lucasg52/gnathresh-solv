import ctypes
import os
_myfun = ctypes.CDLL(os.path.abspath("test.so"))
_myfun.return_input.argtypes = (ctypes.c_voidp, )

