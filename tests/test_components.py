"""Tests for components module."""

import inspect

import pytest

import rolland.components as components_module


def get_classes(module):
    """Return all classes defined in a module."""
    return [cls for name, cls in inspect.getmembers(module, inspect.isclass)]

@pytest.mark.parametrize("cls", get_classes(components_module))
def test_class_initialization(cls):
    """Test class initialization."""
    instance = cls()
    assert isinstance(instance, cls)
