import pytest
from unittest.mock import MagicMock

from entity.bloq import Bloq
from exceptions.bloq_exceptions import BloqNofFound
from usecase.bloq_usecase import BloqUseCase


@pytest.fixture
def mock_bloq_repo():
    return MagicMock()

@pytest.fixture
def bloq_usecase(mock_bloq_repo):
    return BloqUseCase(mock_bloq_repo)

def test_create_bloq(bloq_usecase, mock_bloq_repo):
    # Arrange
    bloq = Bloq(id="bloq-100", title="Test Bloq", address="123 Test St")
    mock_bloq_repo.create.return_value = bloq

    # Act
    result = bloq_usecase.create_bloq(bloq)

    # Assert
    mock_bloq_repo.create.assert_called_once_with(bloq)
    assert result is bloq

def test_list_bloqs(bloq_usecase, mock_bloq_repo):
    # Arrange
    bloq1 = Bloq(id="bloq-1", title="Main Bloq", address="AAA")
    bloq2 = Bloq(id="bloq-2", title="Backup Bloq", address="BBB")
    mock_bloq_repo.get_all.return_value = [bloq1, bloq2]

    # Act
    result = bloq_usecase.list_bloqs()

    # Assert
    mock_bloq_repo.get_all.assert_called_once()
    assert len(result) == 2
    assert result[0].id == "bloq-1"
    assert result[1].id == "bloq-2"

def test_get_bloq_found(bloq_usecase, mock_bloq_repo):
    # Arrange
    bloq = Bloq(id="bloq-1", title="Main Bloq", address="AAA")
    mock_bloq_repo.get_by_id.return_value = bloq

    # Act
    result = bloq_usecase.get_bloq("bloq-1")

    # Assert
    mock_bloq_repo.get_by_id.assert_called_once_with("bloq-1")
    assert result is bloq

def test_get_bloq_not_found(bloq_usecase, mock_bloq_repo):
    # Arrange
    mock_bloq_repo.get_by_id.return_value = None

    # Act / Assert
    with pytest.raises(BloqNofFound) as exc:
        bloq_usecase.get_bloq("bloq-999")
    assert "not found" in str(exc.value).lower()
