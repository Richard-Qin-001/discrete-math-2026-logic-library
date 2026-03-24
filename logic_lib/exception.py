class LogicExprError(Exception):
    def __init__(self, message):
        super().__init__(message)

    def __str__(self):
        return super().__str__()
