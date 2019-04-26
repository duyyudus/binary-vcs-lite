from pathlib2 import Path
from common import util, hashing

_CFG_DICT = util.CFG_DICT

VCS_FOLDER = _CFG_DICT['VCS_FOLDER']
REPO_FOLDER = _CFG_DICT['REPO_FOLDER']
WORKSPACE_FOLDER = _CFG_DICT['WORKSPACE_FOLDER']
BLOB_FOLDER = _CFG_DICT['BLOB_FOLDER']
SESSION_FOLDER = _CFG_DICT['SESSION_FOLDER']
STATE_FOLDER = _CFG_DICT['STATE_FOLDER']

log_info = util.log_info


class Blob(object):
    """Manage data blob."""

    def __init__(self, workdir, repodir):
        """
        Params
        ------
        workdir : str
            A folder with `./VCS_FOLDER/WORKSPACE_FOLDER` as sub-folder
        repodir : str
            A folder with `./VCS_FOLDER/REPO_FOLDER` as sub-folder
        """

        super(Blob, self).__init__()
        self._repodir = repodir
        self._workdir = workdir

    @property
    def blob_dir(self):
        return str(Path(self._repodir, VCS_FOLDER, REPO_FOLDER, BLOB_FOLDER))

    def store_blob(self, verbose=0):
        """
        Put files in working dir to blob

        Params
        ------
        workdir_hash : common.hashing.WorkdirHash

        """

        log_info('Preparing to store blob...')

        workdir_hash = hashing.hash_workdir(self._workdir)
        path_pair = []
        for k in workdir_hash:
            sub_folder = workdir_hash[k]['hash'][:2]
            blob_name = workdir_hash[k]['hash'][2:]
            target = str(Path(self.blob_dir, sub_folder, blob_name))
            path_pair.append((
                workdir_hash[k]['absolute_path'],
                target
            ))
            # log_info(target)

        util.batch_copy(path_pair, verbose)
        log_info('Stored blob')
