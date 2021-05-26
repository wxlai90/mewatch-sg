class Item:
    def __init__(self, **kargs) -> None:
        '''
            name:str
            description:str
            image: str
            params:dict 
        '''
        self.name = kargs['name']
        self.description = kargs['description']
        self.image = kargs['image'] if 'image' in kargs else None
        self.params = kargs['params'] if 'params' in kargs else None
        self.to_play = kargs['to_play'] if 'to_play' in kargs else None

        # params and to_play should be mutually exclusive
        if 'params' in kargs and 'to_play' in kargs:
            raise Exception('only either params or to_play should be defined.')
        
        self.type = 'folder' if 'params' in kargs else 'file'
        self.isFolder = self.type == 'folder'


    def setIsFile(self, b:bool) -> None:
        if b:
            self.type = 'file'
        else:
            self.type = 'folder'

        self.isFolder = self.type == 'folder'