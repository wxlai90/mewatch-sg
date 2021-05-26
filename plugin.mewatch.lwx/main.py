import sys
from lib import router
# import so that it initializes
from controllers import main_controller

def main():
    print(sys.argv)
    if sys.argv[2] != '':
        router.handle(sys.argv[2])
    else:
        router.routes['landing_screen']()


main()