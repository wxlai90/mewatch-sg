from lib import action_builder
from models.item import Item
from services.mewatch import getPage, search
from utils.keyboard import get_user_input


def landing_screen(params = None):
    items = [Item(name="Search", description="Search for a show", params={'path': 'searchAndDisplayResults'})]

    action_builder.createScreen(items)


def searchAndDisplayResults(params = None):
    searchTerm = get_user_input(prompt='Search for a show')
    if not searchTerm:
        return 

    resultsPages = search(searchTerm)

    action_builder.createScreen(resultsPages.items, resultsPages.title)


def listShowEpisodes(params):
    show_path = params['show_path']
    page = getPage(show_path)

    action_builder.createScreen(page.items, page.title)