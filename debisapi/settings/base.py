import os
import warnings
from datetime import datetime, timedelta

from .defaults import *

# Secret Key
__secret_key = os.environ.get("SECRET_KEY", None)

if __secret_key is None:
    warnings.warn(
        "The SECRET_KEY environment variable is not defined."
        " Using default development secret key."
        " Do not forget to set your SECRET_KEY environment variable.",
        RuntimeWarning,
    )
else:
    SECRET_KEY = __secret_key

# Rest
JWT_EXPIRATION = lambda: datetime.utcnow() + timedelta(hours=1)
