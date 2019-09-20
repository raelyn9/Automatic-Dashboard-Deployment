import utility as util

config = util.load_config()

class Visual():
    
    def __init__(self):
        pass

    def read_TEST(self):
        self.id = config['TEST']['ID']
        self.title = config['TEST']['TITLE']
        self.dataset = config['TEST']['DATASET']
        self.database = config['TEST']['DATABASE']
        self.table = config['TEST']['TABLE']
        self.workspace = config['TEST']['WORKSPACE']
        self.connection = config['TEST']['CONNECTION']

    def read_PROD(self):
        self.id = config['PROD']['ID']
        self.title = config['PROD']['TITLE']
        self.dataset = config['PROD']['DATASET']
        self.database = config['PROD']['DATABASE']
        self.table = config['PROD']['TABLE']
        self.workspace = config['PROD']['WORKSPACE']
        self.connection = config['PROD']['CONNECTION']


def load_test_config():
    visual = Visual()
    visual.read_TEST()
    return visual

def load_prod_config():
    visual = Visual()
    visual.read_PROD()
    return visual