while True:
    try:
        exec(open("./palace_monitor.py").read())
    except Exception as e:
        print('Exception occured: ', e)