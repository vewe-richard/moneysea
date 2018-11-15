from utils.stockidname import StockIdName

class Global:
    INSTANCE = None

    def __init__(self):
        if self.INSTANCE is not None:
            raise ValueError("An instantiation already exists!")
        self.sin = StockIdName()

    @classmethod
    def get_instance(cls):
        if cls.INSTANCE is None:
            cls.INSTANCE = Global()
        return cls.INSTANCE



if __name__ == "__main__":
    glb = Global.get_instance()
    print glb.sin.getname(300230)
    pass
