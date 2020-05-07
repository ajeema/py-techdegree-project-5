from os import path
import os
import webbrowser

def main():
    check()

def check():
    check = path.exists('env')
    if check is True:
        start_app()
    else:
        start_setup()

def start_setup():
    print("Let's get you setup and configured")
    os.system("python3 -m venv ./env")


def start_app():
    print("Let's skip setup and go!")
    os.system("python3 app.py")


if __name__ =="__main__":
    main()