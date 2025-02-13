class RentError(Exception):
    pass

class FailedToCreateRent(RentError):
    def __init__(self):
        self.message = f"Failed to create rent."
        super().__init__(self.message)

class RentAlreadyExists(RentError):
    def __init__(self, rent_id: str):
        self.message = f"Rent {rent_id} already exists."
        super().__init__(self.message)


class RentNotFound(RentError):
    def __init__(self, rent_id: str):
        self.message = f"Rent {rent_id} not found."
        super().__init__(self.message)


class InvalidStatus(RentError):
    def __init__(self, current_status: str, expected_status: str):
        self.message = f"Invalid status! Current status is {current_status}, expected {expected_status}."
        super().__init__(self.message)


class RentNotFoundDuringUpdate(RentError):
    def __init__(self, rent_id: str):
        self.message = f"Rent {rent_id} not found during update."
        super().__init__(self.message)
