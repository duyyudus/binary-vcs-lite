from binary_vcs_lite.common.util import *
from binary_vcs_lite.common import hashing
from binary_vcs_lite.core.repo import Repo

_vcs_logger = VcsLogger()
log_info = _vcs_logger.log_info
log_debug = _vcs_logger.log_debug
log_error = _vcs_logger.log_error


class WorkspaceNotFound(VcsLiteError):
    """There is no repo folder."""

    def __init__(self, message='', vcs_logger=None):
        super(WorkspaceNotFound, self).__init__(message, vcs_logger)


class InvalidWorkspace(VcsLiteError):
    """There is no METADATA file."""

    def __init__(self, message='', vcs_logger=None):
        super(InvalidWorkspace, self).__init__(message, vcs_logger)


class Workspace(object):
    """Manage working directory.

    Controls which files to track using glob/regex file patterns
    and handle workspace-related operations

    It must connect to a `core.repo.Repo`

    Attributes:
        _file_pattern (dict):
        _workspace_dir (Path):
        _deep_dir (Path):
        _metadata_path (Path):
        _session_id (str):
        _revision (int):
        _repo (Repo):

    Properties:
        file_pattern (dict):
        workspace_dir (Path):
        deep_dir (Path):
        session_id (str):
        revision (int):
        repo_id (str):
        workspace_hash (common.hashing.WorkspaceHash):
        is_dirty (bool):

    Methods:
        set_file_pattern(file_pattern)
        connect_repo(repo, session_id)
        absolute_path(hash_value)
        commit(session_list, data, add_only, fast_forward)
        checkout(session_id, revision, checkout_dir=None, overwrite=False)
        save()
        load()
        detect_revision()
        latest_revision(session_id)
        all_revision(session_id)
        all_session()
        detail_file_version(session_id, revision, relative_path)
        ls_changes()
        compare_revision(session_1, revision_1, session_2, revision_2)

    """

    def __init__(self, workspace_dir, repo, session_id, init=0):
        """
        Args:
            workspace_dir (str|Path): Any folder with sub-hierarchy `VCS_FOLDER/WORKSPACE_FOLDER`
            repo (Repo):
            session_id (str):
            init (bool):

        """
        super(Workspace, self).__init__()
        check_type(workspace_dir, [str, Path])
        check_type(repo, [Repo])
        check_type(session_id, [str])

        workspace_dir = Path(workspace_dir)
        check_path(workspace_dir)

        self._workspace_dir = workspace_dir
        self._deep_dir = self._workspace_dir.joinpath(VCS_FOLDER, WORKSPACE['FOLDER'])
        self._metadata_path = self._deep_dir.joinpath(WORKSPACE['METADATA']['FILE'])

        if init and not self._metadata_path.exists():
            self._deep_dir.mkdir(parents=1, exist_ok=1)
        elif not self._deep_dir.exists():
            self._enable_log()
            raise WorkspaceNotFound('WorkspaceNotFound: {}'.format(self._deep_dir.as_posix()), _vcs_logger)
        elif not self._metadata_path.exists():
            self._enable_log()
            raise InvalidWorkspace('InvalidWorkspace: {}'.format(self._deep_dir.as_posix()), _vcs_logger)

        self._enable_log()

        make_hidden(self._deep_dir.parent, _vcs_logger)

        self.connect_repo(repo, session_id)
        self.set_file_pattern(DEFAULT_FILE_PATTERN)

    def _enable_log(self):
        log_file = Path(self._deep_dir, LOG_FOLDER, '_{}_{}.txt'.format(
            os.environ['username'],
            time.strftime('%Y-%m-%d')
        ))
        _vcs_logger.setup(log_file, Path(__file__).stem)

    @property
    def file_pattern(self):
        """dict: """
        return self._file_pattern

    @property
    def workspace_dir(self):
        """Path: """
        return self._workspace_dir

    @property
    def deep_dir(self):
        """Path: """
        return self._deep_dir

    @property
    def metadata_path(self):
        """Path: """
        return self._metadata_path

    @property
    def session_id(self):
        """str: ID of current session."""
        return self._session_id

    @property
    def revision(self):
        """int: current revision of `self.session_id`."""
        return self._revision

    @property
    def repo_id(self):
        """str: """
        return self._repo.repo_id

    @property
    def workspace_hash(self):
        """WorkspaceHash: """
        return hashing.hash_workspace(
            self._workspace_dir,
            file_pattern=self._file_pattern,
            vcs_logger=_vcs_logger
        )

    @property
    def is_dirty(self):
        """bool: check if there is any change between current workspace and current revision of current session."""
        changes = self.ls_changes()
        changes.pop('unchanged')
        for c in changes.values():
            if c:
                return 1
        return 0

    def set_file_pattern(self, file_pattern):
        """
        Args:
            file_pattern (dict):
        """
        check_type(file_pattern, [dict])
        self._file_pattern = file_pattern

    def connect_repo(self, repo, session_id):
        """
        Args:
            repo (Repo):
            session_id (str):
        """
        check_type(repo, [Repo])
        check_type(session_id, [str])

        self._repo = repo
        self.load()
        self._session_id = session_id
        self._revision = self.detect_revision()
        self.save()
        log_info(' ')
        log_info('Connected to repo: {}'.format(repo.repo_id))
        log_info('----{}'.format(repo.repo_dir))

    def absolute_path(self, hash_value):
        """
        Args:
            hash_value (str):
        Returns:
            str:
        """
        check_type(hash_value, [str])
        return self.workspace_hash.hash_to_path(hash_value)

    def commit(self, session_list, data, add_only, fast_forward):
        """
        Args:
            session_list (list of str):
            data (dict):
            add_only (bool):
            fast_forward (bool):
        """
        check_type(session_list, [list])
        check_type(data, [dict])

        current_session_id = self.session_id
        current_revision = self.revision

        log_info('Commit ::')
        log_info('----session_list: {}'.format(str(session_list)))
        log_info('----add_only: {}'.format(add_only))
        log_info('----fast_forward: {}'.format(fast_forward))
        log_info('----current_session_id: {}'.format(current_session_id))
        log_info('----current_revision: {}'.format(current_revision))

        if fast_forward and current_session_id in session_list:
            current_revision = self._repo.latest_revision(current_session_id)
            self._revision = current_revision

        state_in_succeed = self._repo.state_in(
            self.workspace_hash,
            session_list,
            data,
            current_session_id,
            current_revision,
            add_only
        )
        if state_in_succeed:
            if current_session_id in session_list:
                self._revision += 1
                self.save()

        log_info('Commit succeed')

    def checkout(self, session_id, revision, checkout_dir=None, overwrite=False):
        """
        Args:
            session_id (str):
            revision (int):
            checkout_dir (Path, None by default):
            overwrite (bool, False by default):
        """
        check_type(session_id, [str])
        check_type(revision, [int])
        check_type(checkout_dir, [str, Path, type(None)])

        log_info('Checkout ::')
        log_info('----session_id: {}'.format(session_id))
        log_info('----revision: {}'.format(revision))
        log_info('----checkout_dir: {}'.format(str(checkout_dir)))
        log_info('----overwrite: {}'.format(str(overwrite)))

        ws_hash = self.workspace_hash
        if checkout_dir:
            ws_hash.set_workspace_dir(checkout_dir)
        state_out_succeed = self._repo.state_out(ws_hash, session_id, revision, overwrite)
        if state_out_succeed:
            self._session_id = session_id
            self._revision = revision
            self.save()

        log_info('Checkout succeed')

    def save(self):
        """Save workspace info to METADATA file."""

        repo_record_key = WORKSPACE['METADATA']['REPO_RECORD_KEY']
        path_key = WORKSPACE['METADATA']['PATH_KEY']
        session_id_key = WORKSPACE['METADATA']['SESSION_ID_KEY']
        revision_key = WORKSPACE['METADATA']['REVISION_KEY']

        data = load_json(self._metadata_path, _vcs_logger)
        if repo_record_key in data:
            repo_record = data[repo_record_key]
        else:
            repo_record = {}
        repo_record[self.repo_id] = {
            path_key: self._repo.repo_dir.as_posix(),
            session_id_key: self._session_id,
            revision_key: self._revision
        }
        data[repo_record_key] = repo_record
        save_json(data, self._metadata_path, _vcs_logger)

    def load(self):
        """Load workspace info from METADATA file."""

        repo_record_key = WORKSPACE['METADATA']['REPO_RECORD_KEY']
        session_id_key = WORKSPACE['METADATA']['SESSION_ID_KEY']
        revision_key = WORKSPACE['METADATA']['REVISION_KEY']

        data = load_json(self._metadata_path, _vcs_logger)
        if repo_record_key not in data:
            return
        repo_record = data[repo_record_key]
        if self.repo_id in repo_record:
            self._session_id = repo_record[self.repo_id][session_id_key]
            self._revision = repo_record[self.repo_id][revision_key]

    def detect_revision(self):
        """Detect revision for current session.

        If recorded in METADATA and valid, use that value, otherwise use latest revision from repo

        Returns:
            int:
        """
        repo_record_key = WORKSPACE['METADATA']['REPO_RECORD_KEY']
        session_id_key = WORKSPACE['METADATA']['SESSION_ID_KEY']
        revision_key = WORKSPACE['METADATA']['REVISION_KEY']

        data = load_json(self._metadata_path, _vcs_logger)

        log_debug('Detect Revision ::')
        log_debug(data)

        if repo_record_key in data:
            repo_record = data[repo_record_key]
            if self.repo_id in repo_record:
                repo_history = repo_record[self.repo_id]
                if revision_key in repo_history:
                    if repo_history[session_id_key] == self._session_id:
                        revision = repo_history[revision_key]
                        if revision <= self.latest_revision(self._session_id):
                            return revision

        return self.latest_revision(self._session_id)

    def latest_revision(self, session_id):
        """Wrap same method in `self._repo`

        Args:
            session_id (str):

        Returns:
            int:
        """
        return self._repo.latest_revision(session_id)

    def all_revision(self, session_id):
        """Wrap same method in `self._repo`

        Args:
            session_id (str):

        Returns:
            list of int:
        """
        return self._repo.all_revision(session_id)

    def all_session(self):
        """Wrap same property in `self._repo`

        Returns:
            list of str:
        """
        return self._repo.all_session

    def detail_file_version(self, session_id, revision=None, relative_path=None):
        """Wrap same method in `self._repo`

        Args:
            session_id (str):
            revision (int, None by default):
            relative_path (str|Path, None by default):

        Returns:
            dict:
        """
        return self._repo.detail_file_version(session_id, revision, relative_path)

    def ls_changes(self):
        """Detect changes between current workspace and current revision of current session

        Returns:
            dict:
        """
        return self._repo.ls_changes(
            self.workspace_hash,
            self._session_id,
            self._revision
        )

    def compare_revision(self, session_1, revision_1, session_2, revision_2):
        """Return difference from one revision of session 2 to another revision of session 1

        Equally as the transition from one revision of session 1 to one revision of session 2

        Args:
            session_1 (str): ID of session 1
            revision_1 (int): revision of session 1
            session_2 (str): ID of session 2
            revision_2 (int): revision of session 2

        Returns:
            dict:
        """
        s1_id = self._repo._session_manager.get_session(session_1).revision_data[str(revision_1)]
        s2_id = self._repo._session_manager.get_session(session_2).revision_data[str(revision_2)]
        s1 = self._repo._state_chain.get_state(s1_id)
        s2 = self._repo._state_chain.get_state(s2_id)
        return self._repo._state_chain.compare_state(s1, s2, return_path=1)
