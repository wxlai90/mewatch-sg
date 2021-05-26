import sys
from lib import router
from controllers.main_controller import landing_screen, searchAndDisplayResults, listShowEpisodes

# register (path, func)
# TODO: refactor into decorator
# @Controller, parse the list of handlers, sanity check, no duplicate key when adding to routes dict
router.register('landing_screen', landing_screen)
router.register('searchAndDisplayResults', searchAndDisplayResults)
router.register('listShowEpisodes', listShowEpisodes)


def main():
    print(sys.argv)
    if sys.argv[2] != '':
        router.handle(sys.argv[2])
    else:
        landing_screen()


main()