"""Flake8 checks for the ROS package."""

from ament_flake8.main import main_with_errors


def test_flake8() -> None:
    rc, errors = main_with_errors(argv=[])
    assert rc == 0, '\n'.join(errors)
