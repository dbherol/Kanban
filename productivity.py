# https://www.semicolonworld.com/question/56593/finding-the-current-active-window-in-mac-os-x-using-python
# https://www.youtube.com/watch?v=ZBLYcvPl1MA
# https://realpython.com/python-dicts
# https://www.youtube.com/watch?v=TbMKwl11itQ
# https://stackoverflow.com/questions/2957116/make-2-functions-run-at-the-same-time
# https://realpython.com/python-dicts/

from pynput.keyboard import Key, Listener
from AppKit import NSWorkspace
from threading import Thread
import time

words = 0;
totalTime = 0;
totalWords = 0;
activityDict = {}

def words_typed():
    def on_press(key):
        global words
        if key == Key.space:
            words+=1

    def on_release(key):
        if key == Key.esc:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def get_active_window():
    def calculate_activity_totals(activity_totalTime, currentAppName):
        global activityDict, words, totalTime, totalWords

        if currentAppName in activityDict.keys():
            activity_totalTime += activityDict[currentAppName][0]
            words += activityDict[currentAppName][1]

        # https://www.geeksforgeeks.org/python-summation-of-tuple-dictionary-values/
        totals = tuple(sum(x) for x in zip(*activityDict.values()))

        if totals:
            totalTime = totals[0]
            totalWords = totals[1]

        timePercent = calculate_percent(activity_totalTime,totalTime)
        wordPercent = calculate_percent(words,totalWords)
        activityDict[currentAppName] = (activity_totalTime, words, timePercent, wordPercent)

        for key in activityDict:
            timePercent = calculate_percent(activityDict[key][0],totalTime)
            wordPercent = calculate_percent(activityDict[key][1],totalWords)
            activityDict[key] = (activityDict[key][0], activityDict[key][1], timePercent, wordPercent)

    global activityDict, words
    currentAppName = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']
    start = time.time()

    while True:
        activeAppName = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']
        if currentAppName != activeAppName:
            end = time.time()
            activity_totalTime = end - start
            calculate_activity_totals(activity_totalTime, currentAppName)
            start = time.time()
            currentAppName = activeAppName
            words = 0
            print(activityDict)


def calculate_percent(part, whole):
    if part != 0:
        if whole != 0 and part/whole < 1:
            return(part/whole)*100
        return 100
    return 0

def main():
    Thread(target = words_typed).start()
    Thread(target = get_active_window).start()

if __name__ == '__main__':
    main()
