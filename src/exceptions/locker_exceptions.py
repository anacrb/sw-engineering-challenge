class LockerError(Exception):
    pass


class FailedToCreateLocker(LockerError):
    def __init__(self):
        self.message = "Failed to create locker."
        super().__init__(self.message)


class LockerAlreadyExists(LockerError):
    def __init__(self, locker_id: str):
        self.message = f"Locker {locker_id} already exists."
        super().__init__(self.message)

class LockerNotFound(LockerError):
    def __init__(self, locker_id: str):
        self.message = f"Locker {locker_id} not found."
        super().__init__(self.message)

class FailedToUpdateLocker(LockerError):
    def __init__(self):
        self.message = "Failed to update locker."
        super().__init__(self.message)