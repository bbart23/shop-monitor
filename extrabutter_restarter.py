import time
while True:
    try:
        exec(open("./extrabutter_monitor.py").read())
    except Exception as e:
        print('Exception occured: ', e)
        time.sleep(10)