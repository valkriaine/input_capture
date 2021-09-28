# Wang Yifei T00609917
# This program captures key-down and key-up events and their durations
# as well as the total input time for any user input
# the data will be stored in a list of arrays
from pynput import keyboard
import time

# global float variables for key timestamps
start_press = 0
start_release = 0

start_input = 0  # total input time

# key-down and key-up toggles
key_pressed = False  # no key is pressed when the program starts
key_released = True  # all keys are released when the program starts

data = []


# called when a key is pressed
def on_press(key):
    try:
        global key_released
        global key_pressed
        global start_press
        global start_release
        global start_input
        global data

        # if no key is being pressed, start recording the key-press event
        if not key_pressed:
            key_pressed = True  # a key is pressed
            key_released = False  # a key is pressed, therefore not released
            start_press = time.time()  # start of key-press
            if not start_release == 0:  # at least one key has been pressed before
                release_duration = time.time() - start_release  # record the last key-release interval
                data.append(["key-up", "key-up duration: " + format(release_duration)])
            else:  # no key has been pressed before
                start_input = time.time()  # start of all inputs

    except AttributeError:
        print('special key pressed: {0}'.format(
            key))


#  called when a key has been released
def on_release(key):
    global key_released
    global key_pressed
    global start_press
    global start_release
    global start_input
    global data

    key_pressed = False  # key released, therefore no key is pressed
    key_released = True  # key released

    start_release = time.time()  # start of key-release
    press_duration = time.time() - start_press  # end of key-press
    # print("Key-down time is {}".format(press_duration))

    data.append([format(key), "key-down duration: " + format(press_duration)])

    if key == keyboard.Key.enter:  # enter key pressed
        # Stop listener
        total_duration = time.time() - start_input  # end of all inputs
        print_to_file(total_duration)
        return False


# Collect events until enter is pressed
def start_monitor():
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()


# print data to file
def print_to_file(total_duration):
    # print index
    with open("output.txt", 'r') as fr:
        x = len(fr.readlines())

    # append data
    with open("output.txt", "a") as fa:
        print(x + 1, end=": ", file=fa)
        for x in range(len(data)):
            print(data[x], end=" ", file=fa)
        print("Total input time: {}".format(total_duration), end="\n", file=fa)


start_monitor()
