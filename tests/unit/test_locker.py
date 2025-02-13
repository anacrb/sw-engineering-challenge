import pytest
from unittest.mock import MagicMock

from entity.locker import Locker, LockerStatus
from exceptions.locker_exceptions import LockerNotFound
from usecase.locker_usecase import LockerUseCase


@pytest.fixture
def mock_locker_repo():
    return MagicMock()

@pytest.fixture
def locker_usecase(mock_locker_repo):
    return LockerUseCase(mock_locker_repo)

def test_create_locker(locker_usecase, mock_locker_repo):
    locker = Locker(id="locker-10", bloqId="bloq-1", status=LockerStatus.CLOSED, isOccupied=False)
    mock_locker_repo.create.return_value = locker

    result = locker_usecase.create_locker(locker)
    mock_locker_repo.create.assert_called_once_with(locker)
    assert result is locker

def test_list_lockers(locker_usecase, mock_locker_repo):
    l1 = Locker(id="locker-1", bloqId="bloq-1", status=LockerStatus.OPEN, isOccupied=False)
    l2 = Locker(id="locker-2", bloqId="bloq-2", status=LockerStatus.CLOSED, isOccupied=True)
    mock_locker_repo.get_all.return_value = [l1, l2]

    result = locker_usecase.list_lockers()
    assert len(result) == 2

def test_update_locker_not_found(locker_usecase, mock_locker_repo):
    # Arrange
    updated_data = Locker(id="locker-999", bloqId="bloq-1", status=LockerStatus.OPEN, isOccupied=True)
    mock_locker_repo.get_by_id.return_value = None

    # Act / Assert
    with pytest.raises(LockerNotFound) as exc:
        locker_usecase.update_locker("locker-999", updated_data)
    assert "not found" in str(exc.value).lower()
