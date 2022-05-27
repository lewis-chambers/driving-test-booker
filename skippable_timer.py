import msvcrt
import time


def timer(threshold=10):

    counter = 0

    print("Waiting for %i seconds" % threshold)

    while True:
        if msvcrt.kbhit() == 1:
            if str(msvcrt.getch()) == 'b\'\\r\'':
                broken = True
                break
        elif counter >= threshold:
            broken = False
            break
        # do something else
        print(".")
        time.sleep(1)
        counter = counter + 1

    if broken:
        while msvcrt.kbhit():
            msvcrt.getch()

    return broken
    
if __name__ == '__main__':
    timer(10)