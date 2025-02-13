import pytest
from unittest.mock import MagicMock
from datetime import datetime, timezone

from entity.locker import Locker
from entity.rent import Rent, RentStatus
from exceptions.rent_exceptions import InvalidStatus
from usecase.rent_usecase import RentUseCase


@pytest.fixture
def mock_rent_repo():
    return MagicMock()

@pytest.fixture
def mock_locker_repo():
    return MagicMock()

@pytest.fixture
def rent_usecase(mock_rent_repo, mock_locker_repo):
    return RentUseCase(mock_rent_repo, mock_locker_repo)


def test_dropoff_parcel_success(rent_usecase, mock_rent_repo, mock_locker_repo):
    rent = Rent(
        id="rent-1",
        lockerId="locker-1",
        weight=2.0,
        size="M",
        status=RentStatus.CREATED,
        createdAt=datetime.now(timezone.utc)
    )
    # Mock existing rent
    mock_rent_repo.get_by_id.return_value = rent
    # Return updated rent in update
    updated_rent = rent.model_copy(update={"status": RentStatus.WAITING_PICKUP, "droppedOffAt": datetime.now(timezone.utc)})
    mock_rent_repo.update.return_value = updated_rent

    # Mock locker
    locker = Locker(id="locker-1", bloqId="bloq-1", status="CLOSED", isOccupied=False)
    mock_locker_repo.get_by_id.return_value = locker

    # Act
    result = rent_usecase.dropoff_parcel("rent-1")

    # Assert
    mock_rent_repo.get_by_id.assert_called_once_with("rent-1")
    mock_rent_repo.update.assert_called_once()
    mock_locker_repo.get_by_id.assert_called_once_with("locker-1")
    mock_locker_repo.update.assert_called_once()
    assert result.status == RentStatus.WAITING_PICKUP

def test_dropoff_parcel_invalid_status(rent_usecase, mock_rent_repo):
    rent = Rent(
        id="rent-2",
        lockerId="locker-1",
        weight=2.0,
        size="M",
        status=RentStatus.WAITING_PICKUP,
        createdAt=datetime.now(timezone.utc)
    )
    mock_rent_repo.get_by_id.return_value = rent

    with pytest.raises(InvalidStatus) as exc:
        rent_usecase.dropoff_parcel("rent-2")
    assert "invalid status" in str(exc.value).lower()

def test_pickup_parcel_success(rent_usecase, mock_rent_repo, mock_locker_repo):
    rent = Rent(
        id="rent-10",
        lockerId="locker-10",
        weight=5.0,
        size="L",
        status=RentStatus.WAITING_PICKUP,
        createdAt=datetime.now(timezone.utc),
        droppedOffAt=datetime.now(timezone.utc)
    )
    mock_rent_repo.get_by_id.return_value = rent
    updated_rent = rent.model_copy(update={"status": RentStatus.DELIVERED, "pickedUpAt": datetime.now(timezone.utc)})
    mock_rent_repo.update.return_value = updated_rent

    # Locker
    locker = Locker(id="locker-10", bloqId="bloq-1", status="CLOSED", isOccupied=True)
    mock_locker_repo.get_by_id.return_value = locker

    result = rent_usecase.pickup_parcel("rent-10")
    assert result.status == RentStatus.DELIVERED
    mock_rent_repo.update.assert_called_once()
    mock_locker_repo.update.assert_called_once()
