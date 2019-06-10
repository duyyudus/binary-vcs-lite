from binary_vcs_lite.common.util import *
from binary_vcs_lite.common import hashing
from binary_vcs_lite.common.hashing import WorkspaceHash
from .state import StateTree
from .blob import Blob
from .state_chain import StateChain
from .session_manager import SessionManager


class RepoNotFound(VcsLiteError):
    """There is no repo folder."""


class InvalidRepo(VcsLiteError):
    """Missing required subfolder of components under repo."""


class OutOfDate(VcsLiteError):
    """Current revision is older than the latest one."""


class Repo(object):
    """Manage version control system repository.

    Controls components::

        `core.blob.Blob`
        `core.state_chain.StateChain`
        `core.session_manager.SessionManager`

    Attributes:
        _repo_dir (Path):
        _deep_dir (Path):
        _repo_id (Path):
        _metadata_path (Path):
        _blob_dir (Path):
        _session_dir (Path):
        _state_dir (Path):
        _blob (core.blob.Blob):
        _session_manager (core.session_manager.SessionManager):
        _state_chain (core.state_chain.StateChain):

    Properties:
        repo_dir (Path):
        deep_dir (Path):
        repo_id (str):
        metadata_path (Path):

    Methods:
        state_in(target_wh,
                 session_list,
                 data,
                 current_session_id,
                 current_revision,
                 add_only)
        state_out(target_wh, session_id, revision, overwrite)
        save()
        load()
        latest_revision(session_id)
        all_revision(session_id)
        all_session()
        detail_file_version(session_id, revision=None, relative_path=None)

    """

    def __init__(self, repo_dir, init=0):
        """
        Args:
            repo_dir (str|Path):
            init (bool):
        Raises:
            RepoNotFound:
            InvalidRepo:

        """
        super(Repo, self).__init__()
        check_type(repo_dir, [str, Path])

        repo_dir = Path(repo_dir)
        self._repo_dir = repo_dir
        self._deep_dir = self._repo_dir.joinpath(VCS_FOLDER, REPO['FOLDER'])
        self._blob_dir = self._deep_dir.joinpath(BLOB['FOLDER'])
        self._state_dir = self._deep_dir.joinpath(STATE['FOLDER'])
        self._session_dir = self._deep_dir.joinpath(SESSION['FOLDER'])

        if init and not self._deep_dir.exists():
            self._blob_dir.mkdir(exist_ok=1)
            self._state_dir.mkdir(exist_ok=1)
            self._session_dir.mkdir(exist_ok=1)
            self._repo_id = '{}_{}_{}'.format(
                os.environ['username'],
                time.strftime('%Y%m%d'),
                time.strftime('%H%M')
            )
            self.save()
        elif not repo_dir.exists():
            raise RepoNotFound()
        elif not (self._blob_dir.exists() and self._state_dir.exists() and self._session_dir.exists()):
            raise InvalidRepo()

        self._metadata_path = self._repo_dir.joinpath(REPO['METADATA']['FILE'])
        self.load()
        self._blob = Blob(self._blob_dir)
        self._state_chain = StateChain(self._state_dir)
        self._session_manager = SessionManager(self._session_dir, self._state_chain)

    @property
    def repo_dir(self):
        """Path: """
        return self._repo_dir

    @property
    def deep_dir(self):
        """Path: """
        return self._deep_dir

    @property
    def repo_id(self):
        """str: """
        return self._repo_id

    @property
    def metadata_path(self):
        """Path: """
        return self._metadata_path

    def state_in(self,
                 target_wh,
                 session_list,
                 data,
                 current_session_id,
                 current_revision,
                 add_only):
        """
        Args:
            target_wh (WorkspaceHash):
            session_list (list of str):
            data (dict):
            current_session_id (str):
            current_revision (int):
            add_only (bool):
        Raises:
            OutOfDate:
        Returns:
            bool:
        """
        check_type(target_wh, [WorkspaceHash])
        check_type(session_list, [list])
        check_type(data, [dict])
        check_type(current_session_id, [str])
        check_type(current_revision, [int])

        if current_revision < self.session_data[current_session_id].latest_revision:
            raise OutOfDate()

        new_state = self._state_chain.new_state(target_wh, session_list, data, save=0)
        current_state = self.get_state(current_session_id, current_revision)
        state_diff = self._state_chain.compare_state(current_state, new_state, return_path=0)

        if add_only:
            # Create a temp state tree using a list of file nodes in `current_state`
            tmp_state_files = current_state.state_tree.ls_all_leaves(with_data=1, as_path=1, relative=1)
            tmp_state_tree = StateTree(
                hashing.workspace_hash_from_paths(tmp_state_files)
            )

            # Add new nodes to temp state tree
            for n in state_diff['added']:
                if not tmp_state_tree.contain_path(n.nice_path):
                    tmp_state_tree.add_path(n.path_with_data(relative=0))

            # Modify data of corresponding node of temp state to modified node of new state
            for n in state_diff['modified']:
                tn = tmp_state_tree.search(n.nice_path)
                if tn:
                    tn[0].set_data(n.data)

            # Set temp state tree as state tree for the new state
            new_state._state_tree = tmp_state_tree

            # Reduce `target_wh` to `added/modifed/unchanged` files only
            for n in state_diff['renamed']:
                if n in target_wh:
                    target_wh.pop(n)
            for n in state_diff['moved']:
                if n in target_wh:
                    target_wh.pop(n)
            for n in state_diff['copied']:
                if n in target_wh:
                    target_wh.pop(n)

        self._blob.store(target_wh)
        new_state.save()
        self._session_manager.update_session(current_session_id)
        return 1

    def state_out(self, target_wh, session_id, revision, overwrite):
        """
        Args:
            target_wh (WorkspaceHash):
            session_id (str):
            revision (int):
            overwrite (bool):
        Returns:
            bool:
        """
        check_type(target_wh, [WorkspaceHash])
        check_type(session_id, [str])
        check_type(revision, [int])

        s = self.get_state(session_id, revision)
        state_wh = s.to_workspace_hash()
        if not overwrite:
            for f in target_wh:
                if f in state_wh:
                    state_wh.pop(f)

        state_wh.set_workspace_dir(target_wh.workspace_dir)
        self._blob.extract(state_wh)
        return 1

    def save(self):
        """Save repo info to METADATA file."""

        repo_id_key = REPO['METADATA']['REPO_ID_KEY']
        data = {}
        data[repo_id_key] = self.repo_id
        save_json(data, self.metadata_path)

    def load(self):
        """Load repo info to METADATA file."""

        repo_id_key = REPO['METADATA']['REPO_ID_KEY']
        data = load_json(self.metadata_path)
        self._repo_id = data[repo_id_key]

    def latest_revision(self, session_id):
        """
        Args:
            session_id (str):

        Returns:
            int:
        """
        return self._session_manager.latest_revision(session_id)

    def all_revision(self, session_id):
        """
        Args:
            session_id (str):

        Returns:
            list of int:
        """
        return self._session_manager.all_revision(session_id)

    def all_session(self):
        """
        Returns:
            list of str:
        """
        return self._session_manager.all_session_id

    def detail_file_version(self, session_id, revision=None, relative_path=None):
        """
        Args:
            session_id (str):
            revision (int, None by default):
            relative_path (str|Path, None by default):

        Returns:
            dict:
        """
        return self._session_manager.detail_file_version(
            session_id,
            revision,
            relative_path
        )
