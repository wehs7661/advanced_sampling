"""
Unit and regression test for the advanced_sampling package.
"""

# Import package, test suite, and other packages as needed
import advanced_sampling
import pytest
import sys

def test_advanced_sampling_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "advanced_sampling" in sys.modules
