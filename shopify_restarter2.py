import time
while True:
    try:
        exec(open("./shopify_driver2.py").read())
    except Exception as e:
        print('Exception occured: ', e)
        time.sleep(10)