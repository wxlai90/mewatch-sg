import requests
from typing import List
from models.playable import Playable
from models.page import Page
from models.episode import Episode
from models.item import Item
from resolvers.mewatch import resolvePage, resolveSearch, resolveShows


def getPage(show_path: str) -> Page:
    api_response = resolvePage(show_path)

    raw_episodes = api_response['item']['episodes']['items']
    
    paging = api_response['item']['episodes']['paging']

    if 'next' in paging:
        # there are more than 1 page to resolve
        season_id = api_response['item']['id']
        raw_episodes = _paginationSearch(season_id, 2, raw_episodes)

    items = [Item(name=i['episodeName'], description= i['shortDescription'], image=i['images']['tile'],to_play=i['offers'][0]['scopes'][0]) for i in raw_episodes]

    page = Page(title = api_response['title'], items = items)

    return page


def _paginationSearch(season_id: int, page_no: int, previous: list) -> List[dict]:
    '''
        recursive calling of api to get all episodes that have been paginated
    '''

    headers = {
        'Accept': 'application/json',
        'Referer': 'https://www.mewatch.sg/',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    }

    url = f'https://cdn.mewatch.sg/api/items/{season_id}/children?ff=idp%2Cldp%2Crpt%2Ccd&lang=en&page={page_no}&page_size=50&segments=all'

    response = requests.get(url, headers=headers)

    page_resp = response.json()

    # base case
    if len(page_resp['items']) == 0:
        return previous

    accumulated = previous + page_resp['items']

    return _paginationSearch(season_id, page_no + 1, accumulated)


def search(searchTerm: str) -> Page:
    search_results = resolveSearch(searchTerm)

    # TODO: iterate through all possible fields instead of using only tv
    tv_items = search_results['tv']['items']


    if len(tv_items) == 0:
    # no search results found
        return Page(title = f'Search Results for {searchTerm}', items = [])


    multiple_seasons = tv_items[0]['availableSeasonCount'] > 1

    if multiple_seasons:
        # more than one season, traverse and find all shows in a season before listing
        pageJSON = resolvePage(tv_items[0]['path'])
        seasons = pageJSON['item']['show']['seasons']['items']
        items = []
        items = [Item(name=season['title'], description=season['shortDescription'], image=season['images']['tile'], params={'path': 'listShowEpisodes', 'show_path': season['path']}) for season in seasons]
    else:
        # only one season, display show directly
        items = [Item(name=i['secondaryLanguageTitle'] if 'secondaryLanguageTitle' in i else i['title'], description=i['shortDescription'], image=i['images']['tile'], params={'path':'listShowEpisodes', 'show_path': i['path']}) for i in tv_items]

    page = Page(title = f'Search Results for {searchTerm}', items = items)

    return page



def resolveShowIdToVideo(show_id) -> Playable:
    raw_shows = resolveShows(show_id)

    selected_subs = []
    selected_source = None

    # TODO: extract into dedicated parser.
    for show in raw_shows:
        if show['name'] == 'HLS_Web':
            selected_source = show['url']

        # older shows have no subtitles
        if 'subtitles' in show:
            if show['subtitles']['English'] not in selected_subs:
                selected_subs.append(show['subtitles']['English'])

        
    playable = Playable(url = selected_source, subtitles = selected_subs)

    return playable