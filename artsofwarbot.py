from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage
import os
import logging
import random
import sys
from datetime import datetime

BUTTONS_PATH = 'artsofwarbot/buttons'
LOOP_SECONDS = 4
TOUCH_PADDING = 3
MAX_UNKNOWN_SNAPS = 30

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
        'x': 904,
        'y': 2101,
        'width': 116,
        'height': 70,
        'imgfile': 'ability-off-fight.png',
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
        'x': 543,
        'y': 1440,
        'width': 336,
        'height': 105,
        'imgfile': 'next-level-defeted.png',
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

unknownSnapsCnt = 0

def processLoopAction():
    global unknownSnapsCnt
    snap = device.takeSnapshot()
    for button in buttons:
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
            return

    unknownSnapsCnt += 1
    if unknownSnapsCnt == MAX_UNKNOWN_SNAPS:
        logging.info("unknown screen snap")
        dtStr = datetime.now().strftime("%Y%m%d%H%M%S")
        snap.writeToFile("artsofwarbot/logs/unknown-%s.png" % dtStr,'png')
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
