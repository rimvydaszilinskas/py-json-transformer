class TransformerException(Exception):
    def __init__(self, msg="Transformer exception", key=None, index=None, *args):
        self.key = key
        self.index = index
        self.msg = msg
        super().__init__(msg, *args)

    def __str__(self):
        return f"{self.msg}. Key={self.key}. Index={self.index}"
