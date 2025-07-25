from unittest.mock import MagicMock, Mock, patch

import pytest

from src.app.security import domain as domain_security
from src.app.task.domain import entity as entity_domain
from src.app.task.domain import entity as entity_repository
from src.app.task.domain import repository as domain_repository
from src.app.task.services import board as board_services
from src.domain.models import repository as repository_model
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
        mock_board.inject_member.assert_called_with(
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


class MockBoardRepository(domain_repository.BoardRepository):
    def __init__(self):
        self.boards = {}

    def get_by_id(self, id):
        return self.boards.get(id)

    def update(self, id, to_update):
        if id in self.boards:
            self.boards[id] = to_update

    def create(self, new):
        self.boards[new.id] = new
        return new

    def delete(self, id):
        if id in self.boards:
            del self.boards[id]

    def filter(self, criteria):
        return list(self.boards.values())

    def filter_by_user_id(self, user_id, criteria):
        return list(self.boards.values())

    def serialize(self, data):
        return data


class MockOwnerShipBoardRepository(domain_repository.OwnerShipBoardRepository):

    def __init__(self):
        self.ownerships = []

    def delete_by_user_id_and_board_id(self, user_id: str, board_id: str) -> None:
        self.ownerships = [
            o
            for o in self.ownerships
            if o.user_id != user_id and o.board_id != board_id
        ]

    def get_by_board_id(self, board_id):
        return [o for o in self.ownerships if o.board_id == board_id]

    def get_by_id(self, id):
        for ownership in self.ownerships:
            if ownership.id == id:
                return ownership
        return None

    def get_by_user_id_and_board_id(self, user_id, board_id):
        for ownership in self.ownerships:
            if ownership.user_id == user_id and ownership.board_id == board_id:
                return ownership
        return None

    def create(self, new):
        self.ownerships.append(new)
        return new

    def update(self, id, to_update):
        for i, ownership in enumerate(self.ownerships):
            if ownership.id == id:
                self.ownerships[i] = to_update
                return

    def update_role_by_user_id_and_board_id(
        self, user_id: str, board_id: str, to_update: entity_domain.RoleMemberType
    ) -> None:
        for i, ownership in enumerate(self.ownerships):
            if ownership.user_id == user_id and board_id == board_id:
                ownership.role = to_update
                return

    def delete(self, id):
        self.ownerships = [o for o in self.ownerships if o.id != id]

    def filter(self, criteria):
        return self.ownerships

    def serialize(self, data):
        return data


class MockLogAdapter(LogAdapter):
    def _message(self, msg, status):
        pass


@pytest.fixture
def mock_dependencies():
    mock_board_repo = MockBoardRepository()
    mock_ownership_repo = MockOwnerShipBoardRepository()
    mock_logger = MockLogAdapter(None)

    board = entity_repository.Board.create(
        id="mock-board-id",
        name="Original Board Name",
        description="Original Board Description",
        user_id="admin-user",
    )

    board.inject_member(
        entity_repository.BoardMember(
            user_id="non-admin-user",
            board_id="mock-board-id",
            role=entity_repository.RoleMemberType.VIEWER,
        )
    )

    mock_board_repo.boards["mock-board-id"] = board

    mock_ownership_repo.ownerships.append(
        domain_repository.OwnerShipRepositoryData(
            id="ownership-1",
            user_id="non-admin-user",
            board_id="mock-board-id",
            role=entity_repository.RoleMemberType.VIEWER,
        )
    )

    return mock_board_repo, mock_ownership_repo, mock_logger


def test_update_board_success(mock_dependencies):
    mock_board_repo, mock_ownership_repo, mock_logger = mock_dependencies
    payload = board_services.UpdateBoardCommandRequest(
        name="Updated Board Name",
        description="Updated Board Description",
        icon_url="new-icon-url",
    )

    result = board_services.update_board(
        payload=payload,
        user_id="admin-user",
        board_id="mock-board-id",
        repository_board=mock_board_repo,
        repository_ownership=mock_ownership_repo,
        logger=mock_logger,
    )

    updated_board = mock_board_repo.get_by_id("mock-board-id")
    assert updated_board.name == "Updated Board Name"
    assert updated_board.description == "Updated Board Description"
    assert updated_board.icon_url == "new-icon-url"
    assert result.name == "Updated Board Name"


def test_update_board_not_admin(mock_dependencies):
    mock_board_repo, mock_ownership_repo, mock_logger = mock_dependencies
    payload = board_services.UpdateBoardCommandRequest(
        name="Updated Board Name",
        description="Updated Board Description",
        icon_url=None,
    )

    with pytest.raises(entity_repository.NotAdminOfBoardError):
        board_services.update_board(
            payload=payload,
            user_id="non-admin-user",
            board_id="mock-board-id",
            repository_board=mock_board_repo,
            repository_ownership=mock_ownership_repo,
            logger=mock_logger,
        )


def test_update_nonexistent_board(mock_dependencies):
    mock_board_repo, mock_ownership_repo, mock_logger = mock_dependencies
    payload = board_services.UpdateBoardCommandRequest(
        name="Updated Board Name",
        description="Updated Board Description",
        icon_url=None,
    )

    with pytest.raises(ValueError, match="Board nonexistent-board-id not found"):
        board_services.update_board(
            payload=payload,
            user_id="admin-user",
            board_id="nonexistent-board-id",
            repository_board=mock_board_repo,
            repository_ownership=mock_ownership_repo,
            logger=mock_logger,
        )


def test_delete_board_success():
    mock_board = MagicMock(spec=entity_repository.Board)
    mock_repository_board = MagicMock(spec=domain_repository.BoardRepository)
    mock_repository_ownership = MagicMock(
        spec=domain_repository.OwnerShipBoardRepository
    )
    mock_logger = MagicMock(spec=LogAdapter)

    mock_board.id = "test_board_id"
    mock_repository_board.get_by_id.return_value = mock_board
    mock_board.can_delete.return_value = True

    with patch("src.app.task.services.board.get_board_by_id", return_value=mock_board):
        result = board_services.delete_board(
            board_id="test_board_id",
            user_id="test_user_id",
            repository_board=mock_repository_board,
            repository_ownership=mock_repository_ownership,
            logger=mock_logger,
        )

    assert result == mock_board
    mock_logger.info.assert_called_once_with("Deleting Board")
    mock_board.delete.assert_called_once_with(user_id="test_user_id")
    mock_repository_board.delete.assert_called_once_with(id="test_board_id")


def test_delete_board_not_found():
    mock_repository_board = MagicMock(spec=domain_repository.BoardRepository)
    mock_repository_ownership = MagicMock(
        spec=domain_repository.OwnerShipBoardRepository
    )
    mock_logger = MagicMock(spec=LogAdapter)

    with patch("src.app.task.services.board.get_board_by_id", return_value=None):
        with pytest.raises(ValueError, match="Board test_board_id not found"):
            board_services.delete_board(
                board_id="test_board_id",
                user_id="test_user_id",
                repository_board=mock_repository_board,
                repository_ownership=mock_repository_ownership,
                logger=mock_logger,
            )


def test_delete_board_not_admin(mock_dependencies):
    mock_board_repo, mock_ownership_repo, mock_logger = mock_dependencies

    ownership = domain_repository.OwnerShipRepositoryData(
        id="ownership-1",
        user_id="non-admin-user",
        board_id="mock-board-id",
        role=entity_repository.RoleMemberType.VIEWER,
    )
    mock_ownership_repo.create(ownership)

    with pytest.raises(entity_repository.NotAdminOfBoardError):
        board_services.delete_board(
            board_id="mock-board-id",
            user_id="non-admin-user",
            repository_board=mock_board_repo,
            repository_ownership=mock_ownership_repo,
            logger=mock_logger,
        )


class BoardTestBase:
    BOARD_ID = "test-board-id"
    ADMIN_USER_ID = "admin-user-id"
    NEW_MEMBER_ID = "new-member-id"
    BOARD_NAME = "Test Board"
    BOARD_DESCRIPTION = "Test Description"

    def setUp(self):
        self.mock_board_repo = Mock(spec=domain_repository.BoardRepository)
        self.mock_ownership_repo = Mock(spec=domain_repository.OwnerShipBoardRepository)
        self.mock_user_repo = Mock(spec=domain_security.UserRepository)
        self.mock_logger = Mock(spec=LogAdapter)

        self.mock_user_repo.get_by_id = Mock()

    def create_test_board(self, board_id=None, user_id=None):
        """Helper method to create a test board"""
        return entity_repository.Board.create(
            id=board_id or self.BOARD_ID,
            name=self.BOARD_NAME,
            description=self.BOARD_DESCRIPTION,
            user_id=user_id or self.ADMIN_USER_ID,
        )

    def call_add_member_to_board(self, board_id, user_to_require_change, new_member):
        """Helper method to call the service function"""
        return board_services.add_member_to_board(
            board_id=board_id,
            user_to_require_change=user_to_require_change,
            new_member=new_member,
            repository_board=self.mock_board_repo,
            repository_ownership=self.mock_ownership_repo,
            repository_user=self.mock_user_repo,
            logger=self.mock_logger,
        )


class TestBoardMemberOperations(BoardTestBase):
    def test_add_member_to_board_success(self):
        self.setUp()
        board = self.create_test_board()
        self.mock_board_repo.get_by_id.return_value = board
        self.mock_ownership_repo.get_by_board_id.return_value = []
        self.mock_user_repo.get_by_id.return_value = self.NEW_MEMBER_ID

        result = self.call_add_member_to_board(
            self.BOARD_ID, self.ADMIN_USER_ID, self.NEW_MEMBER_ID
        )
        assert result is not None
        assert result.is_member(
            entity_repository.BoardMember(
                user_id=self.NEW_MEMBER_ID, board_id=self.BOARD_ID
            )
        )

    def test_add_member_to_nonexistent_board(self):
        self.setUp()
        nonexistent_board_id = "nonexistent-board-id"
        self.mock_board_repo.get_by_id.side_effect = (
            repository_model.RepositoryNotFoundError()
        )
        self.mock_ownership_repo.get_by_board_id.return_value = []

        with pytest.raises(ValueError, match=f"Board {nonexistent_board_id} not found"):
            self.call_add_member_to_board(
                nonexistent_board_id, self.ADMIN_USER_ID, self.NEW_MEMBER_ID
            )

    def test_add_nonexistent_member_to_board(self):
        self.setUp()
        nonexistent_member = "nonexistent-member-id"
        board = self.create_test_board()
        self.mock_board_repo.get_by_id.return_value = board
        self.mock_ownership_repo.get_by_board_id.return_value = []
        self.mock_user_repo.get_by_id.side_effect = (
            repository_model.RepositoryNotFoundError()
        )

        with pytest.raises(ValueError, match=f"User {nonexistent_member} not found"):
            self.call_add_member_to_board(
                self.BOARD_ID, self.ADMIN_USER_ID, nonexistent_member
            )

    def test_add_existing_member_to_board(self):
        self.setUp()
        existing_member_id = "existing-member-id"
        board = self.create_test_board()
        existing_member = entity_repository.BoardMember(
            user_id=existing_member_id,
            board_id=self.BOARD_ID,
            role=entity_repository.RoleMemberType.VIEWER,
        )
        board.inject_member(existing_member)
        self.mock_board_repo.get_by_id.return_value = board
        self.mock_ownership_repo.get_by_board_id.return_value = []
        self.mock_user_repo.get_by_id.return_value = existing_member_id

        with pytest.raises(
            entity_repository.HasAlreadyIsMemberError,
            match=f"Member {existing_member_id} already in board {self.BOARD_ID}",
        ):
            self.call_add_member_to_board(
                self.BOARD_ID, self.ADMIN_USER_ID, existing_member_id
            )


def test_update_role_in_member_success():
    board_id = "1234"
    user_to_require_change = "admin_user"
    member_id = "member_user"
    new_role = entity_repository.RoleMemberType.ADMIN

    mock_board = MagicMock(spec=entity_repository.Board)
    mock_board.update_role_member.return_value = None

    repository_board = MagicMock(spec=domain_repository.BoardRepository)
    repository_board.get_by_id.return_value = mock_board

    repository_ownership = MagicMock(spec=domain_repository.OwnerShipBoardRepository)
    repository_ownership.update_role_by_user_id_and_board_id.return_value = None

    logger = MagicMock(spec=LogAdapter)

    repository_board.get_by_id.return_value = mock_board

    result = board_services.update_role_in_member(
        board_id=board_id,
        user_to_require_change=user_to_require_change,
        member_id=member_id,
        new_role=new_role,
        repository_board=repository_board,
        repository_ownership=repository_ownership,
        logger=logger,
    )

    assert result == mock_board
    mock_board.update_role_member.assert_called_once_with(
        member_that_update=user_to_require_change,
        member_id=member_id,
        role=new_role,
    )
    repository_ownership.update_role_by_user_id_and_board_id.assert_called_once_with(
        user_id=member_id, board_id=board_id, to_update=new_role
    )
    logger.info.assert_called_once()


def test_update_role_in_member_board_not_found():
    board_id = "1234"
    user_to_require_change = "admin_user"
    member_id = "member_user"
    new_role = entity_repository.RoleMemberType.EDITOR

    repository_board = MagicMock(spec=domain_repository.BoardRepository)
    repository_board.get_by_id.return_value = None

    repository_ownership = MagicMock(spec=domain_repository.OwnerShipBoardRepository)
    logger = MagicMock(spec=LogAdapter)

    with pytest.raises(ValueError, match=f"Board {board_id} not found"):
        board_services.update_role_in_member(
            board_id=board_id,
            user_to_require_change=user_to_require_change,
            member_id=member_id,
            new_role=new_role,
            repository_board=repository_board,
            repository_ownership=repository_ownership,
            logger=logger,
        )
