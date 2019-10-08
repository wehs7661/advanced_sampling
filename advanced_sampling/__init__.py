"""
advanced_sampling
A proejct for developing simple data analysis methods and illustration of advanced sampling methods used in MD simulations
"""

# Add imports here
from .advanced_sampling import *

# Handle versioneer
from ._version import get_versions
versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions
