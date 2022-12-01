# Gesture Control
#### Leverage mediapipe's hand gesture model and pre-trained model to control computer using gestures
---

### Er Jie Yong
https://www.linkedin.com/in/erjieyong

---

# Introduction
Imagine controlling your computer using gestures alone!

<img src="Images\README\yoda-the-force.gif" width=400/>

# Problem Statement
There are practical uses of gesture control as well when you are not able to access your computer directly such as
- Hands free control when your hands are dirty (eg. Cooking while refering to recipe, turn off the tap)
- Hands free control when you are far away from computer or any input source (eg. controlling the audio from the back of the car, controlling TV without using the remote, controlling presentation slide at a distance without mouse or clicker)
- More flexible control when controlling multi axis objects such as drone
- Gloveless control in Metaverse

There have also been well documented use case of interpreting sign languages to voice or text to facilitate conversation between sign language users and non-users.

# Scope
This project only serve to explore the power of gesture control through transfer learning and to facilitate the ease of user interaction through a user interface. Please contact [me](erjieyong@gmail.com) directly for other requests.

# Capabilities
- Allow window to always stay on top. (allow first time user to familiarise with the gestures while viewing the actions in play)
- Change sleep interval between gesture's actions
- Select from a pre-defined list of action (keystrokes) to run upon detecting the corresponding gestures
- Save the keystrokes locally for futher usage. 
- One-click run to activate the gesture detection and perform actions based on saved settings
- Real time view of webcam and it's predicted gesture
- Real time output of actions performed

<img src="Images\README\Screenshot.png" width=400/><br>


# Showcase


https://user-images.githubusercontent.com/109052378/204944528-68939fc2-7ecd-4310-89af-87f6974f96aa.mp4


<i>Gesture control in action!</i>

# Installation
There are 2 ways to run it

## Easy method
This was made possible using cx_Freeze library
1) Download the zip file from this link: https://bit.ly/3gKBFzC
2) Unzip
3) Double click on Gesture_Control.exe

## Advanced method
1) Clone this repository locally
2) Create a new environment based on requirements.yml
3) Navigate to local folder where this repo is clone and activate the new environment
4) Run `python Gesture_Control.py`

# Reference
- https://techvidvan.com/tutorials/hand-gesture-recognition-tensorflow-opencv/

#### Contact me if you need more advance, accurate gesture control such as using hotkeys or using dual hands
