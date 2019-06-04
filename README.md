# binary-vcs-lite

Minimalism version control system for binary data.

It is designed for versioning asset data in game/3D/VFX industry, in a simple way.

Hopefully, it can make life easier for TA/TD, without using huge version control system like  Perforce.

*Please look at `docs/design.png` for specifications.*

## Target features

### Supported state-diff types between 2 arbitrary states

*Managed by `core.repo.Repo` using  `core.state_chain.StateChain`*

* `added`

* `deleted`

* `modified`

* `unchanged`

* `renamed`

* `moved`

* `copied`

### Versioning session

*Managed by `core.repo.Repo` using `core.session_manager.SessionManager`*

Work on top of `StateChain`, provide a filter-like mechanism to derive a discontinuous sub-chain from main `StateChain` for different working purposes

### Commit modes

*Managed by `core.repo.Repo` using `core.state.State` and `core.state.StateChain`*

* `EXHAUSTIVE` ( default mode, commit all diff types )

* `ADDITIVE` ( also known as `add_only`, commit only `Added`, `Modified`, `Unchanged` diff )

New `State` to be added to `StateChain` is derived differently from `WorkspaceHash` depend on commit modes

Diff calculation process between two `State` objects is always exhaustive

## Main concepts

### `workspace`

Any folder with sub-hierarchy `VCS_FOLDER/WORKSPACE_FOLDER`

`VCS_FOLDER` and `WORKSPACE_FOLDER` can be customized in `./common/config.yml`

Example: We have `../output_data/last/.vcs_lite/.workspace`

* In this case, `../output_data/last` is a valid workspace

### `repo`

Any folder with sub-hierarchy `VCS_FOLDER/REPO_FOLDER`

`VCS_FOLDER` and `REPO_FOLDER` can be customized in `./common/config.yml`

Example: We have `../output_data/last/.vcs_lite/.repo`

* In this case, `../output_data/last` is also a valid repo

**`repo` and `workspace` can be the same folder**

### `vcs_interface`

The main class is `vsc_interface.VersioningInterface`. Users are supposed to use it to interact with `workspace` and `repo`

With 2 subclasses of `VersioningInterface`, we have two working scenarios

* `LocalVersioning`

    `workspace` and `repo` at the same location

* `RemoteVersioning`

    `workspace` and `repo` at the different locations

## Detail

### `workspace` components

* `METADATA`

    It is just the file `VCS_FOLDER/WORKSPACE_FOLDER/METADATA`, store record of all repositories that workspace connected to.

### `repo` components

* `METADATA`

    It is just the file `VCS_FOLDER/REPO_FOLDER/METADATA`, store ID of the repo.

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
