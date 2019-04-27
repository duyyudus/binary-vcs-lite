# binary-vcs-lite

Minimalism version control system for binary data. 

Should work best for graphic data ( model, texture, geometry cache...) as well as non-text files.

## Goals

Supported diff types

* Added

* Removed

* Unchanged

* Renamed

* Moved

## Main concepts

### workspace

Any folder with sub-hierarchy `VCS_FOLDER/WORKSPACE_FOLDER`

`VCS_FOLDER` and `WORKSPACE_FOLDER` can be customized in `./common/config.yml`

Example: We have `../sample_data/last/.vcs_lite/.workspace`

- In this case, `../sample_data/last` is a valid workspace

### repo

Any folder with sub-hierarchy `VCS_FOLDER/REPO_FOLDER`

`VCS_FOLDER` and `REPO_FOLDER` can be customized in `./common/config.yml`

Example: We have `../sample_data/last/.vcs_lite/.repo`

- In this case, `../sample_data/last` is also a valid repo

**`repo` and `workspace` can be the same folder**

### vcs_interface

Users are supposed to use this to interact with `workspace` and `repo`

Two main working scenarios

* `LocalWorking`

    `workspace` and `repo` at the same location

* `RemoteWorking`

    `workspace` and `repo` at the different locations

## Sub concepts

### repo

* blob

    Folder with sub-hierarchy `VCS_FOLDER/REPO_FOLDER/BLOB_FOLDER`

    Store data blobs

* state

    Folder with sub-hierarchy `VCS_FOLDER/REPO_FOLDER/STATE_FOLDER`
    
    Manage states of workspace/working directory

    Skeleton for revisions/versions mechanism

* session

    Folder with sub-hierarchy `VCS_FOLDER/REPO_FOLDER/SESSION_FOLDER`

    Represent for working session

    Work as a filter on top of state chain
