while True:
    try:
        exec(open("./supreme_monitor.py").read())
    except Exception as e:
        print('Exception occured: ', e)