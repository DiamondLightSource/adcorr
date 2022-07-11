from unittest.mock import MagicMock, patch

from numpy import Inf, array, isclose
from numpy.ma import masked_where
from pytest import raises

from adcorr import correct_solid_angle

from .inaccessable_mock import AccessedError, inaccessable_mock


def test_correct_solid_angle_typical_2x2():
    assert isclose(
        array([[1.0075, 2.0150], [3.0225, 4.0300]]),
        correct_solid_angle(
            array([[1.0, 2.0], [3.0, 4.0]]), (1.0, 1.0), (0.1, 0.1), 1.0
        ),
    ).all()


def test_correct_solid_angle_typical_3x3():
    assert isclose(
        array(
            [
                [1.03015, 2.03007, 3.09045],
                [4.06015, 5.0, 6.09022],
                [7.21105, 8.12030, 9.27135],
            ]
        ),
        correct_solid_angle(
            array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]),
            (1.5, 1.5),
            (0.1, 0.1),
            1.0,
        ),
    ).all()


def test_correct_solid_angle_typical_2x2x2():
    assert isclose(
        array(
            [
                [[1.0075, 2.0150], [3.0225, 4.0300]],
                [[5.0375, 6.0451], [7.0526, 8.0601]],
            ]
        ),
        correct_solid_angle(
            array([[[1.0, 2.0], [3.0, 4.0]], [[5.0, 6.0], [7.0, 8.0]]]),
            (1.0, 1.0),
            (0.1, 0.1),
            1.0,
        ),
    ).all()


def test_correct_solid_angle_masked_2x2():
    assert isclose(
        array([[Inf, 2.0150], [3.0225, Inf]]),
        correct_solid_angle(
            masked_where(
                array([[True, False], [False, True]]),
                array([[1.0, 2.0], [3.0, 4.0]]),
            ),
            (1.0, 1.0),
            (0.1, 0.1),
            1.0,
        ).filled(Inf),
    ).all()


def test_correct_solid_angle_passes_beam_center_to_scattering_angles_only():
    with raises(AccessedError):
        correct_solid_angle(
            array([[1.0, 2.0], [3.0, 4.0]]),
            inaccessable_mock(tuple[float, float]),
            (0.1, 0.1),
            1.0,
        )
    with patch(
        "adcorr.solid_angle.scattering_angles",
        MagicMock(return_value=array([[0.5, 0.5], [0.5, 0.5]])),
    ):
        correct_solid_angle(
            array([[1.0, 2.0], [3.0, 4.0]]),
            inaccessable_mock(tuple[float, float]),
            (0.1, 0.1),
            1.0,
        )


def test_correct_solid_angle_passes_pixel_sizes_to_scattering_angles_only():
    with raises(AccessedError):
        correct_solid_angle(
            array([[1.0, 2.0], [3.0, 4.0]]),
            (1.0, 1.0),
            inaccessable_mock(tuple[float, float]),
            1.0,
        )
    with patch(
        "adcorr.solid_angle.scattering_angles",
        MagicMock(return_value=array([[0.5, 0.5], [0.5, 0.5]])),
    ):
        correct_solid_angle(
            array([[1.0, 2.0], [3.0, 4.0]]),
            (1.0, 1.0),
            inaccessable_mock(tuple[float, float]),
            1.0,
        )


def test_correct_solid_angle_passes_distance_to_scattering_angles_only():
    with raises(AccessedError):
        correct_solid_angle(
            array([[1.0, 2.0], [3.0, 4.0]]),
            (1.0, 1.0),
            (0.1, 0.1),
            inaccessable_mock(float),
        )
    with patch(
        "adcorr.solid_angle.scattering_angles",
        MagicMock(return_value=array([[0.5, 0.5], [0.5, 0.5]])),
    ):
        correct_solid_angle(
            array([[1.0, 2.0], [3.0, 4.0]]),
            (1.0, 1.0),
            (0.1, 0.1),
            inaccessable_mock(float),
        )
