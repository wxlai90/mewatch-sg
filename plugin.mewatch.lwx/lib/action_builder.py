import sys
import xbmcplugin
import xbmcgui

from typing import List
from models.item import Item

_baseUrl = sys.argv[0]
_screen = xbmcplugin
_handle = int(sys.argv[1])


def _formatDestination(kwargs):
    '''
        Formats and return query string based on key-value args passed in.
        Path prop is mandatory.
    '''
    params = ''

    for k, v in kwargs.items():
            params += f'&{k}={v}'
            
    # additional # needed for qsl to be recognized properly
    return f'{_baseUrl}#?{params}'



def _resolveDestination(show_id):
    return f'{_baseUrl}#?&path=__handle_show_id_resolve&show_id={show_id}'




def createScreen(items: List[Item], screenTitle:str = None) -> None:
    ''' Takes in a List of Item DTO and creates a screen with them '''

    # sets the title
    _screen.setPluginCategory(_handle, screenTitle if screenTitle else 'meWATCH')

    # sets the type, blanket videos for all videos type
    _screen.setContent(_handle, 'videos')


    # create a list of items and add to screen
    listItems = []

    for item in items:
        listItem = xbmcgui.ListItem()
        listItem.setLabel(item.name)
        listItem.setInfo('video', {
            'plot': item.description
        })

        if item.image:
            listItem.setArt({
                'thumb': item.image,
                'icon': item.image,
                'fanart': item.image
            })

        # format query string using params prop
        if item.isFolder:
            url = _formatDestination(item.params)
        else:
            # is file
            url = _resolveDestination(item.to_play)
            # set IsPlayable property before redirect to resolving
            # otherwise doesn't work.
            listItem.setProperty('IsPlayable', 'true')

        listItems.append((url, listItem, item.isFolder))


    _screen.addDirectoryItems(_handle, listItems)


    # finish populating screen
    # _handle, succeeded, updateListing, cacheToDisc
    _screen.endOfDirectory(_handle, True, False, False)