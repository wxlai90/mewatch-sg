import sys
import xbmcgui
import xbmcplugin

from services.mewatch import resolveShowIdToVideo

_screen = xbmcplugin
_handle = int(sys.argv[1])


def __handle_show_id_resolve(params):
    '''
        internal method to resolve show id to direct link
    '''
    show_id = params['show_id']
    playable = resolveShowIdToVideo(show_id)

    listItem = xbmcgui.ListItem()
    listItem.setPath(playable.url)
    listItem.setSubtitles(playable.subtitles)

    print('playable url:', playable.url)
    print('playable subtitles:', playable.subtitles)

    _screen.setResolvedUrl(_handle, True, listItem)


routes = {
    '__handle_show_id_resolve': __handle_show_id_resolve,
}

def Controller(cls):
    funcs = [i for i in dir(cls) if callable(getattr(cls, i)) and not i.startswith('__')]

    for func in funcs:
        if func in routes:
            raise Exception("Duplicate routes defined! Make sure all handler function names are unique!")
        routes[func] = getattr(cls, func)

    print('routes:', routes)


def _decodeParams(query_string):
    ''' decodes params from query string '''
    ''' ?&path=something&name=okays '''
    props = query_string.split('&')

    props.pop(0) # remove '?' first element

    params = {}

    for keyed_value in props:
        k, v = keyed_value.split('=')
        params[k] = v

    return params


def handle(query_string):
    ''' handles routing, retrieve func to call from routes and call with args '''
    params = _decodeParams(query_string)
    
    print('handle() params:', params)

    if params['path'] not in routes:
        raise Exception('No handler registered for this path [{}]'.format(params['path']))
    
    func = routes[params['path']]
    # might add in logger here.
    # calls func with query_string params
    func(params)