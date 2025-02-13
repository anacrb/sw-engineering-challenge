class BloqError(Exception):
    pass

class FailedToCreatBloq(BloqError):
    def __init__(self):
        self.message = f"Failed to create Bloq."
        super().__init__(self.message)

class BloqAlreadyExists(BloqError):
    def __init__(self, bloq_id: str):
        self.message = f"Bloq {bloq_id} already exists."
        super().__init__(self.message)


class BloqNofFound(BloqError):
    def __init__(self, bloq_id: str):
        self.message = f"Bloq '{bloq_id}' not found."
        super().__init__(self.message)