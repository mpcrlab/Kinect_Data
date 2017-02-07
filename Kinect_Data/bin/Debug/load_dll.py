import ctypes
a = ctypes.cdll.LoadLibrary("Kinect_Data.dll")
print a.init()
print a.start()
print a.getCurrentFrame()
print a.stop()
