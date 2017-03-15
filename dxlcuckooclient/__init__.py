# -*- coding: utf-8 -*-
################################################################################
# Copyright (c) 2017 McAfee Inc. - All Rights Reserved.
################################################################################
from __future__ import absolute_import

from .client import CuckooClient

__version__ = "1.1.0"


def get_version():
    """
    Returns the version of the Cuckoo Client Library

    :return: The version of the Cuckoo Client Library
    """
    return __version__
