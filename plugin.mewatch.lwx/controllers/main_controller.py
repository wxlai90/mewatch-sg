from lib.action_builder import action
from models.item import Item
from services.mewatch import getPage, search
from utils.keyboard import get_user_input
from lib.router import Controller

@Controller
class MainController:
    '''
        Each handler function should return 2 values,
        1. list of items DTO
        2. title, None to use default
    '''
    
    @action(results_in="screen")
    def landing_screen(params = None):
        items = [Item(name="Search", description="Search for a show", params={'path': 'searchAndDisplayResults'})]

        # return None to use default title
        return items, None


    @action(results_in="screen")
    def searchAndDisplayResults(params = None):
        searchTerm = get_user_input(prompt='Search for a show')
        if not searchTerm:
            return 

        resultsPages = search(searchTerm)

        return resultsPages.items, resultsPages.title


    @action(results_in="screen")
    def listShowEpisodes(params):
        show_path = params['show_path']
        page = getPage(show_path)
        
        return  page.items, page.title