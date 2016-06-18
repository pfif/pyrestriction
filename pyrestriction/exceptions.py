class NoNextOperation(Exception):
    pass


class OperationsOnlyMode(UnboundLocalError):
    def __init__(self):
        super(OperationsOnlyMode, self).__init__("In OperationOnly mode, the account only contains Operations and cannot compute values")
