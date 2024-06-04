import ctypes

_scanline = ctypes.CDLL('fileloadlib.so')
_scalline.scanline.argtypes = (ctypes.c_)
