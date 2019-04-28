# binary-vcs-lite

Minimalism version control system for binary data. 

Should work best for graphic data ( model, texture, geometry cache...) as well as non-text files.

## Target features

### Supported state-diff types between 2 arbitrary states

*Managed by `core.repo.Repo` using `core.state.State` and `core.state.StateChain`*

* `Added`

* `Removed`

* `Modified`

* `Unchanged`

* `Renamed`

* `Moved`

### Versioning session

*Managed by `core.repo.Repo` using `core.session.Session`*

Work on top of `StateChain`, provide a filter-like mechanism to derive a discontinuous sub-chain from main `StateChain` for different working purposes

### Commit modes

*Managed by `core.workspace.Workspace`*

* `EXHAUSTIVE` ( commit all diff types )

* `ADDITIVE` ( commit only `Added`, `Modified`, `Unchanged` diff )

New `State` to be added to `StateChain` is derived differently from `WorkspaceHash` depend on commit modes

* In detail, `Workspace` interprets `WorkspaceHash` in `EXHAUSTIVE` or `ADDITIVE` mode, then create a new `State` from interpreted data, and give it to `StateChain`

Real `State` diff calculation process is always exhaustive

## Main concepts

### `workspace`

Any folder with sub-hierarchy `VCS_FOLDER/WORKSPACE_FOLDER`

`VCS_FOLDER` and `WORKSPACE_FOLDER` can be customized in `./common/config.yml`

Example: We have `../sample_data/last/.vcs_lite/.workspace`

- In this case, `../sample_data/last` is a valid workspace

### `repo`

Any folder with sub-hierarchy `VCS_FOLDER/REPO_FOLDER`

`VCS_FOLDER` and `REPO_FOLDER` can be customized in `./common/config.yml`

Example: We have `../sample_data/last/.vcs_lite/.repo`

- In this case, `../sample_data/last` is also a valid repo

**`repo` and `workspace` can be the same folder**

### `vcs_interface`

Users are supposed to use this to interact with `workspace` and `repo`

Two main working scenarios

* `LocalWorking`

    `workspace` and `repo` at the same location

* `RemoteWorking`

    `workspace` and `repo` at the different locations

## Detail

### `repo` components

* `blob`

    Folder with sub-hierarchy `VCS_FOLDER/REPO_FOLDER/BLOB_FOLDER`

    Store data blobs

* `state`

    Folder with sub-hierarchy `VCS_FOLDER/REPO_FOLDER/STATE_FOLDER`
    
    Manage states of workspace/working directory

    Skeleton for versioning mechanism

* `session`

    Folder with sub-hierarchy `VCS_FOLDER/REPO_FOLDER/SESSION_FOLDER`

    Represent for working session

    Work as a filter on top of state chain
