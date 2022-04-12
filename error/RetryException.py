class RetryException(Exception):
    def __init__(self, msg):
        self.msg = msg
        super(RetryException, self).__init__(msg)
