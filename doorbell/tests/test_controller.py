import pytest
import os, glob

# import source.module as mod
# import tests.helpers as hlp
import controller


def test_module_func():
    assert True


def test_controller():
    assert controller.__version__ == "0.1.0a0"
