"""PEP 257 checks for the ROS package."""

from ament_pep257.main import main


def test_pep257() -> None:
    rc = main(argv=['.', 'test'])
    assert rc == 0
