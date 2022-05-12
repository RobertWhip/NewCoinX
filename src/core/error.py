# TODO: implement logic that enables to output custom data

class Error:
    def __init__(self, msg) -> None:
        self.msg = msg

    def __str__(self) -> str:
        return f'An error occured. ERROR CODE: {self.msg}.'
