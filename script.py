# imports
import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
import pyautogui


pyautogui.FAILSAFE = True #failsafe, go to 0, 0

s_key = KeyCode(char='s')  # start and stop key
e_key = KeyCode(char='e')  # exit key


#bounds on screen
start_x = 588
end_x = 1335
start_y = 429
end_y = 1009


def getPos(): #gets the positions
    img = pyautogui.screenshot()
    pix = img.load()

    pos = [] #list of a collection of pixels, all next to each other and have the same color

    for i in range(start_x, end_x):
        for j in range(start_y, end_y):
            pixel = pix[i, j]
            if pixel == (255,219,195): #a target pixel
                has_home = -1 #see if it belongs to a collection previously found
                for z in range(0, len(pos)): #checks every collection
                    collection = pos[z]
                    if abs(collection[len(collection) - 1][0] - i) <= 2 or abs(collection[len(collection) - 1][1] - j) <= 2: #belongs(in proximity)
                        has_home = z #has a home
                        break
                if has_home >= 0:
                    pos[has_home].append([i,j]) #adds to collection
                else:
                    pos.append([[i,j]]) #creates new collection

    allPos = []

    for i in range(0, len(pos)): #gets the near center of every collection
        collection = pos[i]
        middle = int((len(collection) / 2))
        allPos.append(collection[middle])  # adds all

    return allPos


time_diff = 0.450


# mouse click code
class Bot(threading.Thread):  # class that extends threading, allows us to mouse click
    def __init__(self):
        super(Bot, self).__init__()
        self.running = False
        self.program_running = True

    def start_clicking(self):  # start clicking
        self.running = True

    def stop_clicking(self):  # stop clicking
        self.running = False

    def exit(self):  # exit the program
        self.stop_clicking()
        self.program_running = False

    def run(self):  # running
        global time_diff
        while self.program_running:  # program isn't exited
            while self.running: #while the program is running
                pos = getPos() #gets the positions needed to be clicked
                for z in pos:
                    pyautogui.moveTo(z[0], z[1], duration= 0.00001)  # move
                    mouse.click(Button.left, count = 1)
                time.sleep(0.05) #delay in between, needed big time because the actual website must register the click
            time.sleep(0.00001)  # delay


#creates everything
mouse = Controller()  # the mouse
click_thread = Bot()  # thread
click_thread.start()  # starts the thread


#for stopping and starting

def key_press(key):  # key press
    if key == s_key:
        if click_thread.running:
            click_thread.stop_clicking()  # stop
        else:
            click_thread.start_clicking()  # start
    elif key == e_key:  # exit
        click_thread.exit()
        listener.stop()


with Listener(on_press=key_press) as listener:  # listener
    listener.join()
