from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage
import os
import logging
import random
import sys
from datetime import datetime

BUTTONS_PATH = 'artsofwarbot/buttons'
LOOP_SECONDS = 1
TOUCH_PADDING = 3
MAX_UNKNOWN_SNAPS = 180

buttons = [
    {
        'x': 325,
        'y': 1922,
        'width': 420,
        'height': 114,
        'imgfile': 'main-screen-fight.png',
        'img': None
        },
    {
        'x': 332,
        'y': 1930,
        'width': 378,
        'height': 70,
        'imgfile': 'level-start-fight.png',
        'img': None
        },
    {
        'x': 531,
        'y': 1392,
        'width': 357,
        'height': 102,
        'imgfile': 'next-level.png',
        'img': None
        },
    {
        'x': 575,
        'y': 1592,
        'width': 286,
        'height': 77,
        'imgfile': 'next-level-2.png',
        'img': None
        },
    {
        'x': 566,
        'y': 1411,
        'width': 308,
        'height': 71,
        'imgfile': 'next-level-3.png',
        'img': None
        },
    {
        'x': 567,
        'y': 1401,
        'width': 291,
        'height': 78,
        'imgfile': 'next-level-defeted.png',
        'img': None
        },
    {
        'x': 555,
        'y': 1398,
        'width': 327,
        'height': 78,
        'imgfile': 'next-level-defeted-2.png',
        'img': None
        },
    {
        'x': 935,
        'y': 475,
        'width': 57,
        'height': 54,
        'imgfile': 'ads1-close.png',
        'img': None
        },
    {
        'x': 921,
        'y': 756,
        'width': 60,
        'height': 56,
        'imgfile': 'ads2-close.png',
        'img': None
        },
    {
        'x': 966,
        'y': 548,
        'width': 45,
        'height': 47,
        'imgfile': 'ads3-close.png',
        'img': None
        },
    {
        'x': 938,
        'y': 493,
        'width': 51,
        'height': 51,
        'imgfile': 'ads4-close.png',
        'img': None
        },
    {
        'x': 758,
        'y': 736,
        'width': 199,
        'height': 52,
        'imgfile': 'tresure-simple.png',
        'img': None
        },
    {
        'x': 324,
        'y': 1944,
        'width': 438,
        'height': 123,
        'imgfile': 'tresure-simple-fight.png',
        'img': None
        },
    {
        'x': 765,
        'y': 1245,
        'width': 189,
        'height': 56,
        'imgfile': 'tresure-hard.png',
        'img': None
        },
    {
        'x': 755,
        'y': 1760,
        'width': 203,
        'height': 52,
        'imgfile': 'tresure-hard-2.png',
        'img': None
        },
    {
        'x': 105,
        'y': 210,
        'width': 117,
        'height': 129,
        'imgfile': 'run-game.png',
        'img': None
        },
    {
        'x': 103,
        'y': 215,
        'width': 119,
        'height': 124,
        'imgfile': 'run-game-2.png',
        'img': None
        },
    {
        'x': 369,
        'y': 1356,
        'width': 339,
        'height': 90,
        'imgfile': 'reconnect.png',
        'img': None
        },
    {
        'x': 371,
        'y': 1380,
        'width': 334,
        'height': 90,
        'imgfile': 'reconnect-2.png',
        'img': None
        },
    {
        'x': 369,
        'y': 1356,
        'width': 336,
        'height': 93,
        'imgfile': 'reconnect-3.png',
        'img': None
        },
    {
        'x': 552,
        'y': 1581,
        'width': 321,
        'height': 93,
        'imgfile': 'lvl8000-next.png',
        'img': None
        },
    {
        'x': 315,
        'y': 1959,
        'width': 291,
        'height': 93,
        'imgfile': 'lvl8000-fight.png',
        'img': None
        }
]

timeoutButtons = [
    {
        'x': 325,
        'y': 1913,
        'width': 419,
        'height': 121,
        'imgfile': 'cancel-fight.png',
        'img': None
        }
]

logging.basicConfig(
    filename='artsofwarbot/logs/artsofwarbot.log',
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG)

logging.info("Starting ARTS OF WAR bot")

device = MonkeyRunner.waitForConnection()

for button in buttons:
    button['img'] = MonkeyRunner.loadImageFromFile(os.path.join(BUTTONS_PATH, button['imgfile']));

for button in timeoutButtons:
    button['img'] = MonkeyRunner.loadImageFromFile(os.path.join(BUTTONS_PATH, button['imgfile']));

unknownSnapsCnt = 0

def checkButton(snap, button):
    snapButton = snap.getSubImage((button['x'], button['y'], button['width'], button['height']))
    snapSame = snapButton.sameAs(button['img'], 0.9)
    if snapSame:
        unknownSnapsCnt = 0
        touchX = random.randint(button['x'] + TOUCH_PADDING, button['x'] + button['width'] - TOUCH_PADDING)
        touchY = random.randint(button['y'] + TOUCH_PADDING, button['y'] + button['height'] - TOUCH_PADDING)
        sleepSeconds = random.randint(1, 10) / 10.0
        logging.info("touch -> image: %s; x: %d; y: %d; sleepSeconds: %f"
                     % (button['imgfile'], touchX, touchX, sleepSeconds))
        MonkeyRunner.sleep(sleepSeconds)
        device.touch(touchX, touchY, MonkeyDevice.DOWN_AND_UP)
        return True
    return False

def processLoopAction():
    global unknownSnapsCnt
    snap = device.takeSnapshot()
    for button in buttons:
        if checkButton(snap, button):
            return

    unknownSnapsCnt += 1
    if unknownSnapsCnt % MAX_UNKNOWN_SNAPS == 0:
        logging.info("unknown screen snap")
        dtStr = datetime.now().strftime("%Y%m%d%H%M%S")
        snap.writeToFile("artsofwarbot/logs/unknown-%s.png" % dtStr,'png')
        for button in timeoutButtons:
            if checkButton(snap, button):
                break
    pass

def getSnapshot():
    snap = device.takeSnapshot()
    dtStr = datetime.now().strftime("%Y%m%d%H%M%S")
    snap.writeToFile("artsofwarbot/snaps/snap-%s.png" % dtStr,'png')

def runLoop():
    while True:
        processLoopAction();
        MonkeyRunner.sleep(LOOP_SECONDS)    


def printHelp():
    print("Available commands:")
    print("runloop - run infinte loop and checking screen with LOOP_SECONDS interval.")
    print("processaction - execute one iteration of loop and exit")
    print("snapshot - make snapshot and")


if len(sys.argv) < 2:
    printHelp()
elif sys.argv[1] == "runloop":
    runLoop()
elif sys.argv[1] == "processaction":
    processLoopAction()
elif sys.argv[1] == "snapshot":
    getSnapshot()
else:
    printHelp()

logging.info(" ARTS OF WAR end of script")
