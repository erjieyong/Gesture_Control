# Run `python setup.py build` to build the distributable exe
import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["tkinter", "PIL","pathlib","pyautogui","os","cv2","numpy","mediapipe","tensorflow","time","threading","datetime","json"], "include_files":["hand-gesture-recognition-code/","Images/"]}
  
# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name = "Gesture_Control" ,
      version = "1" ,
      description = "Use computer vision to control your computer!" ,
      options={"build_exe": build_exe_options},
      executables = [Executable("Gesture_Control.py")])