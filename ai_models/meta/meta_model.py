class MetaModel:
    ''' Base wrapper class for meta models '''
    def __init__(self, image_to_process):
        self._image_to_process = image_to_process

    def ask(self, prompt:str):
        pass

    @property
    def image_to_process(self):
        return self._image_to_process