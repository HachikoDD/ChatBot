import time


def local_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())



if __name__=="__main__":
    print(local_time())



