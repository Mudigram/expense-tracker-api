"""DEPRECATED: routes moved to `app.api.v1.expenses`

This module is kept for backward compatibility. Importing it will raise
an ImportError to encourage switching to the versioned API.
"""

from warnings import warn

warn_message = (
    "DEPRECATED: use `from app.api.v1.expenses import router` "
    "instead of `app.routes.expenses`. This module will be removed in a future release."
)
warn(warn_message)

raise ImportError(warn_message)

