from typing import Tuple, TypeVar

from numpy import arccos, dtype, power
from numpy.ma import MaskedArray, masked_array

from .utils.geometry import scattering_angles

FrameDType = TypeVar("FrameDType", bound=dtype)
FramesShape = TypeVar("FramesShape", bound=Tuple[int, int, int])


def correct_solid_angle(
    frames: MaskedArray[FramesShape, FrameDType],
    beam_center: Tuple[float, float],
    pixel_sizes: Tuple[float, float],
    distance: float,
) -> MaskedArray[FramesShape, FrameDType]:
    """Corrects for the solid angle by scaling by the inverse of area subtended by a pixel.

    Corrects for the solid angle by scaling by the inverse of area subtended by each
    pixel, as detailed in section 3.4.6 of 'Everything SAXS: small-angle scattering
    pattern collection and correction' [https://doi.org/10.1088/0953-8984/25/38/383201].

    Args:
        frames (MaskedArray[FramesShape, FrameDType]): A stack of frames to be
            corrected.
        beam_center (Tuple[float, float]): The center position of the beam in pixels.
        pixel_sizes (Tuple[float, float]): The real space size of a detector pixel.
        distance (float): The distance between the detector and the sample head.

    Returns:
        MaskedArray[FramesShape, FrameDType]: The corrected stack of frames.
    """
    correction = power(
        arccos(scattering_angles(frames.shape[1:], beam_center, pixel_sizes, distance)),
        3,
    )
    return masked_array(frames / correction, frames.mask)
