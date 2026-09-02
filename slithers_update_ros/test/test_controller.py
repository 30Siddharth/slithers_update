"""Unit tests for simulator-independent controller helpers."""

from types import SimpleNamespace

from slithers_update_ros.controller_node import SlithersController


def test_ordered_positions_uses_configured_joint_order() -> None:
    controller = object.__new__(SlithersController)
    controller.joint_names = ['joint_b', 'joint_a']
    controller.get_logger = lambda: SimpleNamespace(warning=lambda _: None, debug=lambda _: None)
    message = SimpleNamespace(
        name=['joint_a', 'joint_b'],
        position=[1.0, 2.0],
    )
    assert controller._ordered_positions(message) == [2.0, 1.0]


def test_ordered_positions_rejects_incomplete_state() -> None:
    controller = object.__new__(SlithersController)
    controller.joint_names = ['joint_a', 'joint_b']
    controller.get_logger = lambda: SimpleNamespace(warning=lambda _: None, debug=lambda _: None)
    message = SimpleNamespace(name=['joint_a'], position=[1.0])
    assert controller._ordered_positions(message) is None
