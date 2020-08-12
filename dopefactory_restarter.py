import time
while True:
    try:
        exec(open("./dopefactory_monitor.py").read())
    except Exception as e:
        print('Exception occured: ', e)
        time.sleep(10)