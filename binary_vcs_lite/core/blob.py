from binary_vcs_lite.common.util import *
from binary_vcs_lite.common.hashing import (
    WorkspaceHash,
    hash_file
)


class Blob(object):
    """Manage data blob.

    Blob does not care about anything except following info::

        blob_dir (str or Path):
        workspace_hash (common.hashing.WorkspaceHash):

    These data are processed and given to Blob by Workspace and Repo

    Attributes:
        _blob_dir (Path):

    Properties:
        blob_dir (Path):

    Methods:
        store(workspace_hash, verbose=0)
        extract(workspace_hash, verbose=0)

    """

    def __init__(self, blob_dir):
        """
        Args:
            blob_dir (str|Path): A folder store blob data

        """
        check_type(blob_dir, [str, Path])

        super(Blob, self).__init__()
        self._blob_dir = Path(blob_dir)

    @property
    def blob_dir(self):
        """Path: """
        return self._blob_dir

    def _parse_hash(self, hash_value):
        """Parse blob sub folder and blob file name from hash.

        Args:
            hash_value (str): 40-char string digest

        Returns:
            2-tuple: (sub_folder_name, blob_file_name)

        """

        return (hash_value[:2], hash_value[2:])

    def store(self, workspace_hash, verbose=0):
        """Put files in working dir to blob.

        Args:
            workspace_hash (common.hashing.WorkspaceHash):
        Returns:
            list of str:

        """
        check_type(workspace_hash, [WorkspaceHash])

        log_info('Preparing to store blob...')

        path_pair = []
        for v in workspace_hash.values():
            sub_folder, blob_name = self._parse_hash(v[WORKSPACE_HASH['HASH_KEY']])
            blob_file = self._blob_dir.joinpath(sub_folder, blob_name)
            workspace_file = Path(v[WORKSPACE_HASH['ABSOLUTE_PATH_KEY']])
            if workspace_file.exists():
                path_pair.append((workspace_file, blob_file))
                if verbose:
                    log_info('Stored blob: {}/{}'.format(
                        sub_folder,
                        blob_name
                    ))
                    log_info('----{}'.format(str(workspace_file)))

        copied = batch_copy(path_pair, verbose=verbose)
        log_info('Stored all blobs')
        return copied

    def extract(self, workspace_hash, verbose=0):
        """Extract files from blob to working dir.

        Args:
            workspace_hash (common.hashing.WorkspaceHash):
        Returns:
            list of str:

        """
        check_type(workspace_hash, [WorkspaceHash])

        log_info('Preparing to extract blob...')

        path_pair = []
        for v in workspace_hash.values():
            sub_folder, blob_name = self._parse_hash(v[WORKSPACE_HASH['HASH_KEY']])
            blob_file = self._blob_dir.joinpath(sub_folder, blob_name)
            workspace_file = Path(v[WORKSPACE_HASH['ABSOLUTE_PATH_KEY']])
            if blob_file.exists():
                if hash_file(blob_file) != v[WORKSPACE_HASH['HASH_KEY']]:
                    continue
                path_pair.append((blob_file, workspace_file))
                if verbose:
                    log_info('Extracted blob: {}/{}'.format(
                        sub_folder,
                        blob_name
                    ))
                    log_info('----{}'.format(str(workspace_file)))

        copied = batch_copy(path_pair, overwrite=1, verbose=verbose)
        log_info('Extracted all blobs')
        return copied
