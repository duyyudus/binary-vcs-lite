from binary_vcs_lite.common.util import *
from binary_vcs_lite.common import hashing


class Workspace(object):
    """Manage working directory.

    Controls which files to track 
    and handle workspace-related operations

    It must connect to a `core.repo.Repo`

    Attributes:
        _workspace_dir (Path):
        _deep_dir (Path):
        _metadata_path (Path):
        _current_state (str):

    Properties:
        deep_dir (Path):
        workspace_dir (Path):
        workspace_hash (common.hashing.WorkspaceHash):
        current_state (str):

    """

    def __init__(self, workspace_dir, repo, init=0):
        """
        Args:
            workspace_dir (str or Path): Any folder with sub-hierarchy `VCS_FOLDER/WORKSPACE_FOLDER`
            repo (core.repo.Repo)

        """

        super(Workspace, self).__init__()
        self._workspace_dir = Path(workspace_dir)
        self._deep_dir = Path(self._workspace_dir, VCS_FOLDER, WORKSPACE['WORKSPACE_FOLDER'])

        if init:
            self._init_deep_dir()
        else:
            assert self._deep_dir.exists(), 'Invalid Workspace folder'

        self._metadata_path = Path(self._deep_dir, WORKSPACE['METADATA_FILE'])

        self.connect_repo(repo)

    @property
    def deep_dir(self):
        """Path: """
        return self._deep_dir

    @property
    def workspace_dir(self):
        """Path: """
        return self._workspace_dir

    @property
    def workspace_hash(self):
        """common.hashing.WorkspaceHash: """
        return hashing.hash_workspace(self._workspace_dir)

    @property
    def current_state(self):
        """str: """
        return self._current_state

    def _init_deep_dir(self):
        if not self._deep_dir.exists():
            self._deep_dir.mkdir(parents=1)

    def _save_current_state(self, repo_id, repo_dir, current_state):
        metadata = load_json(self._metadata_path)

        if WORKSPACE['REPO_RECORD_KEY'] not in metadata:
            metadata = {
                WORKSPACE['REPO_RECORD_KEY']: {
                    repo_id: {
                        WORKSPACE['PATH_KEY']: str(repo_dir),
                        WORKSPACE['CURRENT_STATE_KEY']: current_state
                    }
                }
            }
        else:
            metadata[WORKSPACE['REPO_RECORD_KEY']][repo_id] = {
                WORKSPACE['PATH_KEY']: str(repo_dir),
                WORKSPACE['CURRENT_STATE_KEY']: current_state
            }
        save_json(metadata, self._metadata_path)

    def _load_current_state(self, repo_id):
        metadata = load_json(self._metadata_path)

        if WORKSPACE['REPO_RECORD_KEY'] not in metadata:
            return None

        record = metadata[WORKSPACE['REPO_RECORD_KEY']]
        if repo_id in record:
            return record[repo_id][WORKSPACE['CURRENT_STATE_KEY']]

    def connect_repo(self, repo):
        self._repo = repo

        current_state = self._load_current_state(repo.repo_id)

        if not current_state:
            current_state = repo.latest_state
            self._save_current_state(
                repo.repo_id,
                repo.repo_dir,
                current_state
            )

        self._current_state = current_state

    def absolute_path(self, relative_path):
        """Join relative path and working dir."""

        return Path(self._workspace_dir, relative_path)
