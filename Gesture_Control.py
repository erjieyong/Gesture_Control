from tkinter import *
from PIL import ImageTk, Image
from pathlib import Path
import pyautogui
import os
import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model
from time import sleep
import threading
import datetime
import json

root = Tk()
root.title("Gesture Control")

###################
##    Settings   ##
###################

frame_setting = LabelFrame(root, text = "Settings", width = 780, pady=5)
frame_setting.grid(row=0, column=0)

# We divide the frame into a 26 column grid
for i in range(26):
    frame_setting.columnconfigure(i,{'minsize':30})

# Stay on top check box
checkbox_stay_top = BooleanVar()

def stay_on_top():
    global checkbox_stay_top
    if checkbox_stay_top.get():
        root.attributes('-topmost',True)
    else:
        root.attributes('-topmost',False)

Checkbutton(frame_setting, text="Always stay on top (Windows)", variable=checkbox_stay_top, onvalue=True, offvalue=False, command=stay_on_top).grid(row=0, column = 1, columnspan=10, pady = 5, sticky=W)

# Sleep Interval
sleep_interval = Entry(frame_setting, width=3)
sleep_interval.grid(row=1, column=1, pady = 5)
label_sleep_interval = Label(frame_setting, text = "Sleep interval between gestures' action in seconds").grid(row=1, column=2, columnspan=10,pady=10, sticky=W)

# About info
label_about1 = Label(frame_setting, text="Developed by erjieyong@gmail.com", font="Serif 7").grid(row=0, column = 20, columnspan=5, pady = 5, sticky=E)

# Column labels
label_gesture_name = Label(frame_setting, text = "Name", font="bold 10").grid(row=2, column=1, columnspan=2)
label_gestures = Label(frame_setting, text = "Gestures", font="bold 10").grid(row=2, column=4, columnspan=2)
label_keystroke = Label(frame_setting, text = "Keystroke Assignment", font="bold 10").grid(row=2, column=7, columnspan=5)

label_gesture_name = Label(frame_setting, text = "Name", font="bold 10").grid(row=2, column=14, columnspan=2)
label_gestures = Label(frame_setting, text = "Gestures", font="bold 10").grid(row=2, column=17, columnspan=2)
label_keystroke = Label(frame_setting, text = "Keystroke Assignment", font="bold 10").grid(row=2, column=21, columnspan=5)

# Get all gestures from folder
images_gen = Path("./Images").glob("*.png")
images = [str(img) for img in images_gen]
images_name = [str(img)[7:-4] for img in images]

# Display gestures. We need to store the image in a dict otherwise it will be garbage collected
gesture_img_dict = {'name':{}, 'img':{}, 'keystroke':{}}
keystroke_list = ['accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
'browserback', 'browserfavorites', 'browserforward', 'browserhome',
'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12'
'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
'command', 'option', 'optionleft', 'optionright']
for i in range(5):
    # Set name
    gesture_img_dict['name'][i] = Label(frame_setting, text = images_name[i]).grid(row=i+3, column = 1, columnspan = 2)
    gesture_img_dict['name'][i+5] = Label(frame_setting, text = images_name[i+5]).grid(row=i+3, column = 14, columnspan = 2)
    # Set images into 2 separate columns
    gesture_img_dict['img'][i] = ImageTk.PhotoImage(Image.open(images[i]))
    gesture_img_dict['img'][i+5] = ImageTk.PhotoImage(Image.open(images[i+5]))
    Label(frame_setting, image = gesture_img_dict['img'][i]).grid(row = i+3, column = 4, columnspan=2)
    Label(frame_setting, image = gesture_img_dict['img'][i+5]).grid(row = i+3, column = 17, columnspan=2)
    # Set drop down list
    gesture_img_dict['keystroke'][i] = StringVar()
    gesture_img_dict['keystroke'][i+5] = StringVar()
    OptionMenu(frame_setting, gesture_img_dict['keystroke'][i], *keystroke_list).grid(row = i+3, column = 7, columnspan=5)
    OptionMenu(frame_setting, gesture_img_dict['keystroke'][i+5], *keystroke_list).grid(row = i+3, column = 21, columnspan=5)
    
# Set default keystroke values
if os.path.exists('saved_keystrokes.txt'):
    # Get saved keystrokes from txt file in current directory
    with open('.\saved_keystrokes.txt', 'r') as f:
        keystrokes = json.loads(f.readline())
    # update setting keystroke to display according to previous saved value
    gesture_img_dict['keystroke'][0].set(keystrokes["call_me"]) #call_me
    gesture_img_dict['keystroke'][1].set(keystrokes["fist"]) #fist
    gesture_img_dict['keystroke'][2].set(keystrokes["live_long"]) #live_long
    gesture_img_dict['keystroke'][3].set(keystrokes["okay"]) #okay
    gesture_img_dict['keystroke'][4].set(keystrokes["peace"]) #peace
    gesture_img_dict['keystroke'][5].set(keystrokes["rock"]) #rock
    gesture_img_dict['keystroke'][6].set(keystrokes["smile"]) #smile
    gesture_img_dict['keystroke'][7].set(keystrokes["stop"]) #stop
    gesture_img_dict['keystroke'][8].set(keystrokes["thumbs_down"]) #thumbs_down
    gesture_img_dict['keystroke'][9].set(keystrokes["thumbs_up"]) #thumbs_up
    sleep_interval.insert(0, keystrokes["sleep"])
else:
    gesture_img_dict['keystroke'][0].set("volumemute") #call_me
    gesture_img_dict['keystroke'][1].set("playpause") #fist
    gesture_img_dict['keystroke'][2].set("pagedown") #live_long
    gesture_img_dict['keystroke'][3].set("pageup") #okay
    gesture_img_dict['keystroke'][4].set("right") #peace
    gesture_img_dict['keystroke'][5].set("left") #rock
    gesture_img_dict['keystroke'][6].set("printscreen") #smile
    gesture_img_dict['keystroke'][7].set("stop") #stop
    gesture_img_dict['keystroke'][8].set("volumedown") #thumbs_down
    gesture_img_dict['keystroke'][9].set("volumeup") #thumbs_up
    sleep_interval.insert(0, 3)

# Save function to save all the keystroke set
def savefile():    
    path = os.getcwd()+'\saved_keystrokes.txt'
    if path != '':
        with open(path, 'w') as f:
            content = f'{{"call_me":"{gesture_img_dict["keystroke"][0].get()}","fist":"{gesture_img_dict["keystroke"][1].get()}","live_long":"{gesture_img_dict["keystroke"][2].get()}","okay":"{gesture_img_dict["keystroke"][3].get()}","peace":"{gesture_img_dict["keystroke"][4].get()}","rock":"{gesture_img_dict["keystroke"][5].get()}","smile":"{gesture_img_dict["keystroke"][6].get()}","stop":"{gesture_img_dict["keystroke"][7].get()}","thumbs_down":"{gesture_img_dict["keystroke"][8].get()}","thumbs_up":"{gesture_img_dict["keystroke"][9].get()}","sleep":{sleep_interval.get()}}}'
            f.write(content)
        label_saved = Label(frame_setting, text = "Keystrokes Saved", fg='grey')
        label_saved.grid(row = 9, column=0, columnspan=26, pady = 5)

button_save = Button(frame_setting, text = "Save Keystroke", padx=10, pady = 5, command = savefile, width = 10, fg='dark blue')
button_save.grid(row=8, column = 8, columnspan=3)


###################
## Webcam Output ##
###################

# Set new frame for webcam output
frame_webcam = LabelFrame(root, text = "Output", width = 780, pady=5)
frame_webcam.grid(row=1, column=0)

# We divide the frame into a 26 column grid
for i in range(26):
    frame_webcam.columnconfigure(i,{'minsize':30})
    # Label(frame_webcam, text = 'test').grid(row=0, column=i)

# Create new label to hold webcam
label_webcam = Label(frame_webcam)
label_webcam.grid(row=1, column=1, columnspan=14)

# # Create new text to hold prediction output
pred_text = Text(frame_webcam, width=30, height=19, wrap = WORD)
pred_text.grid(row=1, column = 16, columnspan=9)


# initialize mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Load the gesture recognizer model
model = load_model('hand-gesture-recognition-code/mp_hand_gesture')

# Load class names
f = open('hand-gesture-recognition-code/gesture.names', 'r')
classNames = f.read().split('\n')
f.close()


# Initialize the webcam
cap = cv2.VideoCapture(0)

# Initialise variable to determine whether to run check_class function
recheck = True

# Function to run if gesture detected
def check_class(className):
    # call upon global recheck variable
    global recheck, pred_text, keystrokes
    # Get current time
    time_now = datetime.datetime.now().strftime("%H:%M:%S")
    # Get saved keystrokes from txt file in current directory
    if os.path.exists('saved_keystrokes.txt'):
        with open('.\saved_keystrokes.txt', 'r') as f:
            keystrokes = json.loads(f.readline())
    else:
        keystrokes = {"call_me":"volumemute","fist":"playpause","live_long":"pagedown","okay":"pageup","peace":"right","rock":"left","smile":"printscreen","stop":"stop","thumbs_down":"volumedown","thumbs_up":"volumeup","sleep":3}
    
    if className == 'call me' and recheck == True:
        pyautogui.press([keystrokes['call_me']])
        recheck = False
        pred_text.insert(1.0, f"{time_now}: Pressed {keystrokes['call_me']}\n")
        sleep(keystrokes['sleep'])
        recheck = True
    elif className == 'fist' and recheck == True:
        pyautogui.press([keystrokes['fist']])
        recheck = False
        pred_text.insert(1.0, f"{time_now}: Pressed {keystrokes['fist']}\n")
        sleep(keystrokes['sleep'])
        recheck = True
    elif className == 'live long' and recheck == True:
        pyautogui.press([keystrokes['live_long']])
        recheck = False
        pred_text.insert(1.0, f"{time_now}: Pressed {keystrokes['live_long']}\n")
        sleep(keystrokes['sleep'])
        recheck = True
    elif className == 'okay' and recheck == True:
        pyautogui.press([keystrokes['okay']])
        recheck = False
        pred_text.insert(1.0, f"{time_now}: Pressed {keystrokes['okay']}\n")
        sleep(keystrokes['sleep'])
        recheck = True
    elif className == 'peace' and recheck == True:
        pyautogui.press([keystrokes['peace']])
        recheck = False
        pred_text.insert(1.0, f"{time_now}: Pressed {keystrokes['peace']}\n")
        sleep(keystrokes['sleep'])
        recheck = True
    elif className == 'rock' and recheck == True:
        pyautogui.press([keystrokes['rock']])
        recheck = False
        pred_text.insert(1.0, f"{time_now}: Pressed {keystrokes['rock']}\n")
        sleep(keystrokes['sleep'])
        recheck = True
    elif className == 'smile' and recheck == True:
        pyautogui.press([keystrokes['smile']])
        recheck = False
        pred_text.insert(1.0, f"{time_now}: Pressed {keystrokes['smile']}\n")
        sleep(keystrokes['sleep'])
        recheck = True
    elif className == 'stop' and recheck == True:
        pyautogui.press([keystrokes['stop']])
        recheck = False
        pred_text.insert(1.0, f"{time_now}: Pressed {keystrokes['stop']}\n")
        sleep(keystrokes['sleep'])
        recheck = True
    elif className == 'thumbs down' and recheck == True:
        pyautogui.press([keystrokes['thumbs_down']])
        recheck = False
        pred_text.insert(1.0, f"{time_now}: Pressed {keystrokes['thumbs_down']}\n")
        sleep(keystrokes['sleep'])
        recheck = True
    elif className == 'thumbs up' and recheck == True:
        pyautogui.press([keystrokes['thumbs_up']])
        recheck = False
        pred_text.insert(1.0, f"{time_now}: Pressed {keystrokes['thumbs_up']}\n")
        sleep(keystrokes['sleep'])
        recheck = True
        

def run():
    # disable the save and run button once webcam has run
    if button_run["state"] == "normal":
        button_run["state"] = "disabled"
        button_save["state"] = "disabled"

    def show_frames():
        # Read each frame from the webcam
        _, frame = cap.read()

        x, y, c = frame.shape

        # Flip the frame vertically
        frame = cv2.flip(frame, 1)
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Get hand landmark prediction
        result = hands.process(framergb)
        
        className = ''

        # post process the result
        if result.multi_hand_landmarks:
            landmarks = []
            for handslms in result.multi_hand_landmarks:
                for lm in handslms.landmark:
                    # print(id, lm)
                    lmx = int(lm.x * x)
                    lmy = int(lm.y * y)

                    landmarks.append([lmx, lmy])

                # Drawing landmarks on frames
                mp_drawing.draw_landmarks(
                    frame,
                    handslms,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

                # Predict gesture
                prediction = model.predict([landmarks])
                # print(prediction)
                classID = np.argmax(prediction)
                className = classNames[classID]

        # show the prediction on the frame
        cv2.putText(frame, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)

        if recheck:
            # run threading so that check_class can be run asynchronously in the background
            t = threading.Thread(target=check_class, args=(className,))
            t.start() # start child thread


        # Show the final output
        # https://stackoverflow.com/questions/62293077/why-is-pils-image-fromarray-distorting-my-image-color
        new_frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # resize to desired size
        new_frame_rgb = cv2.resize(new_frame_rgb, (400, 300))
        imgtk = ImageTk.PhotoImage(image = Image.fromarray(new_frame_rgb))
        label_webcam.imgtk = imgtk
        label_webcam.configure(image=imgtk)
        # Repeat after an interval to capture continiously
        label_webcam.after(20, show_frames)
    show_frames()


# A save button in the setting frame to run the webcam and prediction only upon clicked
button_run = Button(frame_setting, text = "Run", padx=10, pady = 5, command = run, width = 10, fg='dark green')
button_run.grid(row=8, column = 16, columnspan=3)

# loop through root and check changes
root.mainloop()