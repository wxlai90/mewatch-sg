class Episode:
    def __init__(self, **kwargs) -> None:
        '''
            id is technically an int, but using str for versatility 
        '''
        self.name = kwargs['name']
        self.id = kwargs['id']
        self.description = kwargs['description']