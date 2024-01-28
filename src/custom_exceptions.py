# class ConfigFileNotFoundError(Exception):
#     def __init__(self, path, *args):
#         super().__init(args)
#         self.config_path = path
#     def __str__(self):
#         return f"The file:\f{self.config_path}\ndoes not exists"

class InvalidIntervalError(Exception):
    min_intvl = 10
    max_intvl = 30
    def __init__(self, itvl, *args):
        super().__init__(args)
        self.itvl = itvl
    def __str__(self):
        return f"{self.itvl} is not in a valid range {self.min_intvl, self.max_intvl}"

class InvalidStoringPath(Exception):
    def __init__(self, path, *args):
        super().__init__(args)
        self.path = path
    def __str__(self):
        return f"The folder:\n{self.path}\nis not a folder and/or not exists"

class InvalidMaxNumber(Exception):
    min_val = 10
    max_val = 300
    def __init__(self, nbr, *args):
        super().__init__(args)
        self.number = nbr
    def __str__(self):
        return f"{self.number} is not in a valid range {self.min_val, self.max_val}"