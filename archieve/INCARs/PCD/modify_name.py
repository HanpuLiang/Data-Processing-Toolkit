
import os

if __name__ == '__main__':
    files = os.listdir('./')
    for item in files:
        if 'PARCHG' in item:
            new_name = 'CHGCAR%s'%((item.split('.'))[1])
            os.rename(item, new_name)
