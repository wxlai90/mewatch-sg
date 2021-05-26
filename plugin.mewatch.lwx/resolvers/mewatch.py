# DAOs
import requests


def resolvePage(show_path: str) -> dict:
    headers = {
        'Accept': 'application/json',
        'Referer': 'https://www.mewatch.sg/',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    }

    url = f'https://cdn.mewatch.sg/api/page?ff=idp%2Cldp%2Crpt%2Ccd&item_detail_expand=all&item_detail_select_season=first&lang=en&list_page_size=24&max_list_prefetch=3&path={show_path}&segments=all&sub=Anonymous&text_entry_format=html'

    response = requests.get(url, headers=headers)
    
    r = response.json()

    return r


def resolveSearch(searchTerm: str) -> dict:
    headers = {
        'authority': 'cdn.mewatch.sg',
        'accept': 'application/json',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'origin': 'https://www.mewatch.sg',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.mewatch.sg/',
        'accept-language': 'en-US,en;q=0.9',
    }

    params = (
        ('ff', 'idp,ldp,rpt,cd'),
        ('group', 'true'),
        ('lang', 'en'),
        ('segments', 'all'),
        ('term', searchTerm),
    )

    response = requests.get('https://cdn.mewatch.sg/api/search', headers=headers, params=params)

    search_results = response.json()

    return search_results


def resolveShows(show_id: str) -> dict:
    headers = {
        'Accept': 'application/json',
        'Referer': 'https://www.mewatch.sg/',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    }

    url = f'https://cdn.mewatch.sg/api/items/{show_id}/videos?delivery=stream%2Cprogressive&ff=idp%2Cldp%2Crpt%2Ccd&lang=en&resolution=External&segments=all'

    response = requests.get(url, headers=headers)
  
    raw_shows = response.json()

    return raw_shows