#!/usr/bin/env python3
"""Render a motion-smoothed 60 fps version of THE NECKLACE SNAP.

Feathered temporal interpolation creates continuous in-between motion from the
approved storyboard, while an identity lock keeps the face calm and consistent.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import cv2
import imageio_ffmpeg
import numpy as np

from render_necklace_snap import make_foley

ROOT = Path(__file__).resolve().parents[1]
FPS = 60
DURATION = 8.0
WORK_SIZE = (540, 960)
OUTPUT_SIZE = (1080, 1920)

KEYFRAMES = [
    (0.00, "storyboard/frame_01_establishing_closeup.png"),
    (1.54, "storyboard/intermediates/frame_01b_hands_rising.png"),
    (2.08, "storyboard/intermediates/frame_01c_hands_midway_v2.png"),
    (2.45, "storyboard/frame_02_fingers_hooking.png"),
    (3.02, "storyboard/intermediates/frame_02b_grip_set.png"),
    (3.47, "storyboard/frame_03_tension.png"),
    (3.70, "storyboard/frame_04_snap.png"),
    (4.22, "storyboard/intermediates/frame_04b_initial_burst.png"),
    (5.22, "storyboard/frame_05_pearl_explosion.png"),
    (6.45, "storyboard/intermediates/frame_05b_settling.png"),
    (7.56, "storyboard/frame_06_final_pearls_fall.png"),
    (8.00, "storyboard/frame_06_final_pearls_fall.png"),
]


def smoothstep(value: float) -> float:
    value = min(1.0, max(0.0, value))
    return value * value * (3.0 - 2.0 * value)


def load_frame(path: Path) -> np.ndarray:
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(path)
    height, width = image.shape[:2]
    target_ratio = WORK_SIZE[0] / WORK_SIZE[1]
    crop_width = min(width, int(round(height * target_ratio)))
    crop_height = int(round(crop_width / target_ratio))
    x = (width - crop_width) // 2
    y = max(0, (height - crop_height) // 2)
    image = image[y : y + crop_height, x : x + crop_width]
    return cv2.resize(image, WORK_SIZE, interpolation=cv2.INTER_LANCZOS4)


def identity_mask() -> np.ndarray:
    """Softly lock the central face while leaving hair, hands and jewelry free."""
    width, height = WORK_SIZE
    mask = np.zeros((height, width), dtype=np.float32)
    cv2.ellipse(mask, (width // 2, 290), (150, 245), 0, 0, 360, 1.0, -1)
    mask = cv2.GaussianBlur(mask, (0, 0), 31)
    return np.clip(mask[..., None] * 0.90, 0.0, 0.90)


def temporal_blend(
    first: np.ndarray,
    second: np.ndarray,
    amount: float,
) -> np.ndarray:
    """Blend clean keyframes continuously without the rubbery warping of raw flow."""
    amount = smoothstep(amount)
    # A soft temporal integration reads as deliberate 240 fps motion blur while
    # keeping fingers, pearls and facial features structurally intact.
    return cv2.addWeighted(first, 1.0 - amount, second, amount, 0.0)


def camera_and_breathing(image: np.ndarray, time: float) -> np.ndarray:
    """Add a subtle continuous push and low-amplitude breathing drift."""
    width, height = WORK_SIZE
    push = smoothstep(min(time / 3.85, 1.0))
    release = smoothstep(max(0.0, (time - 6.6) / 1.4))
    zoom = 1.0 + 0.017 * push - 0.004 * release
    breath = 0.70 * np.sin(2.0 * np.pi * time / 3.7)
    transform = cv2.getRotationMatrix2D((width * 0.5, height * 0.43), 0.0, zoom)
    transform[1, 2] += breath
    return cv2.warpAffine(
        image,
        transform,
        (width, height),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REFLECT_101,
    )


def render(output: Path) -> None:
    images = [load_frame(ROOT / relative_path) for _, relative_path in KEYFRAMES]
    mask = identity_mask()
    identity = images[0].astype(np.float32)

    audio = ROOT / "sound/necklace_snap_foley.wav"
    if not audio.exists():
        make_foley(audio)

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    output.parent.mkdir(parents=True, exist_ok=True)
    command = [
        ffmpeg,
        "-y",
        "-loglevel", "error",
        "-f", "rawvideo",
        "-pix_fmt", "bgr24",
        "-s:v", f"{OUTPUT_SIZE[0]}x{OUTPUT_SIZE[1]}",
        "-r", str(FPS),
        "-i", "-",
        "-i", str(audio),
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-t", f"{DURATION:.3f}",
        "-vf", "eq=contrast=1.018:saturation=0.94:brightness=-0.006,noise=alls=0.45:allf=t,fade=t=in:st=0:d=0.14,fade=t=out:st=7.86:d=0.14",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "17",
        "-profile:v", "high",
        "-level", "4.2",
        "-pix_fmt", "yuv420p",
        "-r", str(FPS),
        "-color_primaries", "bt709",
        "-color_trc", "bt709",
        "-colorspace", "bt709",
        "-c:a", "aac",
        "-b:a", "256k",
        "-ar", "48000",
        "-movflags", "+faststart",
        "-metadata", "title=THE NECKLACE SNAP — Smooth Cut",
        "-metadata", "comment=60 fps motion-smoothed luxury fashion film",
        str(output),
    ]

    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    assert process.stdin is not None
    previous: np.ndarray | None = None
    segment = 0
    try:
        for frame_number in range(round(DURATION * FPS)):
            time = frame_number / FPS
            while segment + 1 < len(KEYFRAMES) - 1 and time >= KEYFRAMES[segment + 1][0]:
                segment += 1
            start = KEYFRAMES[segment][0]
            end = KEYFRAMES[segment + 1][0]
            amount = (time - start) / max(0.001, end - start)
            # Hold, then accelerate sharply into the snap rather than drifting into it.
            if segment == 5:
                amount = amount ** 2.6
            frame = temporal_blend(
                images[segment], images[segment + 1], amount
            ).astype(np.float32)

            # Keep the deadpan facial performance stable without freezing hands/jewelry.
            frame = frame * (1.0 - mask) + identity * mask
            frame = camera_and_breathing(np.clip(frame, 0, 255).astype(np.uint8), time)

            # Restrained temporal integration gives fast pearls and hands natural motion blur.
            if previous is not None:
                blur_weight = 0.16 if 3.45 <= time <= 5.55 else 0.055
                frame = cv2.addWeighted(frame, 1.0 - blur_weight, previous, blur_weight, 0.0)
            previous = frame
            frame = cv2.resize(frame, OUTPUT_SIZE, interpolation=cv2.INTER_LANCZOS4)
            process.stdin.write(frame.tobytes())
    finally:
        process.stdin.close()
    code = process.wait()
    if code:
        raise subprocess.CalledProcessError(code, command)


if __name__ == "__main__":
    target = ROOT / "output/the_necklace_snap_smooth.mp4"
    render(target)
    print(target)
