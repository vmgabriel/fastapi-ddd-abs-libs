from unittest.mock import Mock

import pytest

from src.app.task.domain import entity as entity_repository
from src.app.task.domain import repository as domain_repository
from src.app.task.services import board as board_services
from src.domain.models.repository import RepositoryNotFoundError
from src.infra.log.model import LogAdapter

# Test Environments
VALID_BOARD_ID = "board123"
VALID_USER_ID = "user123"
TEST_BOARD_NAME = "Test Board"
TEST_BOARD_DESCRIPTION = "Test Description"
TEST_ICON_URL = "http://example.com/icon.png"


@pytest.fixture
def mock_board():
    board = Mock(spec=entity_repository.Board)
    board.id = VALID_BOARD_ID
    board.add_member = Mock()
    return board


@pytest.fixture
def mock_board_repository():
    return Mock(spec=domain_repository.BoardRepository)


@pytest.fixture
def mock_ownership_repository():
    return Mock(spec=domain_repository.OwnerShipBoardRepository)


@pytest.fixture
def mock_logger():
    return Mock(spec=LogAdapter)


class TestGetBoardById:
    def test_success(
        self, mock_board, mock_board_repository, mock_ownership_repository
    ):
        mock_board_repository.get_by_id.return_value = mock_board
        mock_ownership_repository.get_by_board_id.return_value = [
            domain_repository.OwnerShipRepositoryData(
                id="",
                user_id=VALID_USER_ID,
                board_id=VALID_BOARD_ID,
                role=entity_repository.RoleMemberType.VIEWER,
            )
        ]

        result = board_services.get_board_by_id(
            VALID_BOARD_ID, mock_board_repository, mock_ownership_repository
        )

        assert result == mock_board
        mock_board.add_member.assert_called_with(
            member=entity_repository.BoardMember(
                user_id=VALID_USER_ID,
                board_id=VALID_BOARD_ID,
                role=entity_repository.RoleMemberType.VIEWER,
            )
        )

    def test_not_found(self, mock_board_repository, mock_ownership_repository):
        mock_board_repository.get_by_id.side_effect = RepositoryNotFoundError

        result = board_services.get_board_by_id(
            "invalid_id", mock_board_repository, mock_ownership_repository
        )

        assert result is None

    def test_no_owners(
        self, mock_board, mock_board_repository, mock_ownership_repository
    ):
        mock_board_repository.get_by_id.return_value = mock_board
        mock_ownership_repository.get_by_board_id.return_value = []

        result = board_services.get_board_by_id(
            VALID_BOARD_ID, mock_board_repository, mock_ownership_repository
        )

        assert result == mock_board
        mock_board.add_member.assert_not_called()


class TestGetMyselfBoardById:
    def test_success(
        self, mock_board, mock_board_repository, mock_ownership_repository
    ):
        mock_board.is_member.return_value = True
        mock_board_repository.get_by_id.return_value = mock_board

        mock_ownership_repository.get_by_board_id.return_value = [
            domain_repository.OwnerShipRepositoryData(
                id="",
                user_id=VALID_USER_ID,
                board_id="",
                role=entity_repository.RoleMemberType.VIEWER,
            )
        ]

        result = board_services.get_myself_board_by_id(
            user_id=VALID_USER_ID,
            board_id=VALID_BOARD_ID,
            repository_board=mock_board_repository,
            repository_ownership=mock_ownership_repository,
        )

        assert result == mock_board
        mock_board.is_member.assert_called_once_with(
            member=entity_repository.BoardMember(
                user_id=VALID_USER_ID,
                board_id=VALID_BOARD_ID,
                role=entity_repository.RoleMemberType.VIEWER,
            )
        )

    def test_not_member(
        self, mock_board, mock_board_repository, mock_ownership_repository
    ):
        mock_board.is_member.return_value = False
        mock_board_repository.get_by_id.return_value = mock_board

        mock_ownership_repository.get_by_board_id.return_value = [
            domain_repository.OwnerShipRepositoryData(
                id="",
                user_id="invalid_user_id",
                board_id="",
                role=entity_repository.RoleMemberType.VIEWER,
            )
        ]

        with pytest.raises(ValueError, match="Board not found"):
            board_services.get_myself_board_by_id(
                user_id=VALID_USER_ID,
                board_id=VALID_BOARD_ID,
                repository_board=mock_board_repository,
                repository_ownership=mock_ownership_repository,
            )


class TestCreateBoard:
    def get_create_board_payload(self):
        return board_services.CreateBoardCommandRequest(
            id=VALID_BOARD_ID,
            name=TEST_BOARD_NAME,
            description=TEST_BOARD_DESCRIPTION,
            icon_url=TEST_ICON_URL,
        )

    def test_success(
        self, mock_board_repository, mock_ownership_repository, mock_logger
    ):
        payload = self.get_create_board_payload()
        mock_board_repository.get_by_id.return_value = None

        mock_ownership_repository.get_by_board_id.return_value = []

        result = board_services.create_board(
            payload=payload,
            user_id=VALID_USER_ID,
            repository_board=mock_board_repository,
            repository_ownership=mock_ownership_repository,
            logger=mock_logger,
        )

        assert isinstance(result, entity_repository.Board)
        assert result.name == TEST_BOARD_NAME
        assert result.description == TEST_BOARD_DESCRIPTION
        assert result.icon_url == TEST_ICON_URL
        assert result.is_member(
            member=entity_repository.BoardMember(
                user_id=VALID_USER_ID,
                board_id="board123",
                role=entity_repository.RoleMemberType.VIEWER,
            )
        )

        mock_logger.info.assert_called_once_with("Creating Board")
        mock_board_repository.create.assert_called_once_with(new=result)
        assert mock_ownership_repository.create.call_count == 1

    def test_already_exists(
        self, mock_board_repository, mock_ownership_repository, mock_logger
    ):
        payload = self.get_create_board_payload()
        mock_board_repository.get_by_id.return_value = Mock(
            spec=entity_repository.Board
        )

        mock_ownership_repository.get_by_board_id.return_value = []

        with pytest.raises(ValueError, match="Board already exists"):
            board_services.create_board(
                payload=payload,
                user_id=VALID_USER_ID,
                repository_board=mock_board_repository,
                repository_ownership=mock_ownership_repository,
                logger=mock_logger,
            )
