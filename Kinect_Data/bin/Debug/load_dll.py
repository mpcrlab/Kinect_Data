import ctypes
a = ctypes.cdll.LoadLibrary("Kinect_Data.dll")
print a.add(3, 5)
