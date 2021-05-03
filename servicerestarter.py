import os
import signal
import subprocess
import threading
import time

MONKEY_RUNNER_DIR = 'D:\\android\\sdk\\tools\\bin'

runLoop = True
proc = None

# batFile = os.path.join(MONKEY_RUNNER_DIR, 'test.bat')
batFile = os.path.join(MONKEY_RUNNER_DIR, 'monkeyrunner.bat')

mylock = threading.Lock()

def runServiceStarter():
  global runLoop
  global proc
  global mylock

  while runLoop:
    with mylock:
      if runLoop:
        proc = subprocess.Popen(
          [batFile, 'artsofwarbot\\artsofwarbot.py', 'runloop'],
          stdout=subprocess.PIPE,
          stderr=subprocess.STDOUT,
          universal_newlines=True,
          cwd=MONKEY_RUNNER_DIR
          )
      else:
        continue

    lineout = proc.stdout.readline()
    while lineout:
      print(lineout)
      if lineout.find('com.android') >= 0:
        print('terminating artsofwarbot and restart after 5 seconds')
        proc.terminate()
        time.sleep(5)
        break
      lineout = proc.stdout.readline()

  return

def handleSignal(signum, frame):
  global runLoop
  global proc
  global mylock

  print('CTRL+C handled')
  with mylock:
    runLoop = False
    if proc:
      proc.terminate()

  return

signal.signal(signal.SIGINT, handleSignal)

runServiceStarter()
