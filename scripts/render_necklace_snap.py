#!/usr/bin/env python3
"""Render THE NECKLACE SNAP from six storyboard frames with bespoke foley."""

from __future__ import annotations

import math
import subprocess
import wave
from pathlib import Path

import imageio_ffmpeg
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_RATE = 48_000
DURATION = 8.0
FPS = 30


def pan_gains(pan: float) -> tuple[float, float]:
    """Equal-power stereo pan, where -1 is left and +1 is right."""
    angle = (pan + 1.0) * math.pi / 4.0
    return math.cos(angle), math.sin(angle)


def band_noise(rng: np.random.Generator, length: int, low: float, high: float) -> np.ndarray:
    source = rng.normal(0.0, 1.0, length)
    spectrum = np.fft.rfft(source)
    frequencies = np.fft.rfftfreq(length, 1.0 / SAMPLE_RATE)
    edge = max(30.0, min(300.0, (high - low) * 0.12))
    mask = np.clip((frequencies - low) / edge, 0.0, 1.0)
    mask *= np.clip((high - frequencies) / edge, 0.0, 1.0)
    result = np.fft.irfft(spectrum * mask, n=length)
    peak = np.max(np.abs(result)) or 1.0
    return result / peak


def make_foley(output: Path) -> None:
    rng = np.random.default_rng(1988)
    sample_count = int(SAMPLE_RATE * DURATION)
    audio = rng.normal(0, 0.00012, (sample_count, 2))

    def add(signal: np.ndarray, start: float, amplitude: float = 1.0, pan: float = 0.0) -> None:
        offset = max(0, int(start * SAMPLE_RATE))
        end = min(sample_count, offset + len(signal))
        if end <= offset:
            return
        left, right = pan_gains(pan)
        signal = signal[: end - offset] * amplitude
        audio[offset:end, 0] += signal * left
        audio[offset:end, 1] += signal * right

    def click(start: float, frequency: float, amplitude: float, pan: float, decay: float = 0.022) -> None:
        length = max(24, int(SAMPLE_RATE * decay * 5.0))
        t = np.arange(length) / SAMPLE_RATE
        attack = np.clip(t / 0.0004, 0.0, 1.0)
        body = (
            np.sin(2 * np.pi * frequency * t)
            + 0.42 * np.sin(2 * np.pi * frequency * 1.91 * t + 0.7)
            + 0.15 * np.sin(2 * np.pi * frequency * 3.2 * t)
        )
        envelope = attack * np.exp(-t / decay)
        add(body * envelope, start, amplitude, pan)

    # 0:00–0:02 — almost silent room tone.

    # 0:02–0:03.35 — fabric movement and delicate contact clicks.
    fabric_length = int(0.72 * SAMPLE_RATE)
    fabric_t = np.arange(fabric_length) / SAMPLE_RATE
    fabric_env = np.sin(np.pi * np.clip(fabric_t / 0.72, 0, 1)) ** 1.8
    fabric = band_noise(rng, fabric_length, 90, 1_100) * fabric_env
    add(fabric, 1.92, 0.035, -0.18)
    add(fabric[::-1], 2.10, 0.026, 0.24)
    for time, freq, amp, pan in [
        (2.34, 3_050, 0.043, -0.48),
        (2.51, 4_200, 0.034, 0.40),
        (2.72, 3_620, 0.047, -0.12),
        (2.91, 4_780, 0.034, 0.55),
        (3.13, 3_340, 0.027, -0.35),
    ]:
        click(time, freq, amp, pan)

    # 0:03.25–0:03.63 — thread tension, then a short pocket of silence.
    tension_duration = 0.34
    t = np.arange(int(tension_duration * SAMPLE_RATE)) / SAMPLE_RATE
    frequency = 155 + 690 * (t / tension_duration) ** 1.7
    phase = 2 * np.pi * np.cumsum(frequency) / SAMPLE_RATE
    tension_env = np.sin(np.pi * t / tension_duration) ** 1.1
    tension_noise = band_noise(rng, len(t), 220, 2_500)
    tension = (0.62 * np.sin(phase) + 0.38 * tension_noise) * tension_env
    add(tension, 3.25, 0.055, 0.0)

    # 0:03.70 — hero snap: a dry high crack with a physical low transient.
    snap_duration = 0.22
    t = np.arange(int(snap_duration * SAMPLE_RATE)) / SAMPLE_RATE
    crack = band_noise(rng, len(t), 350, 13_500) * np.exp(-t / 0.018)
    low_body = np.sin(2 * np.pi * (105 - 28 * t) * t) * np.exp(-t / 0.055)
    mid_body = np.sin(2 * np.pi * 680 * t) * np.exp(-t / 0.028)
    snap = 0.74 * crack + 0.42 * low_body + 0.25 * mid_body
    snap[0] += 0.9
    add(np.tanh(snap * 1.35), 3.70, 0.72, 0.0)

    # 0:03.78–0:04.55 — pearls rush close to the lens.
    whoosh_duration = 0.76
    t = np.arange(int(whoosh_duration * SAMPLE_RATE)) / SAMPLE_RATE
    whoosh_env = np.sin(np.pi * np.clip(t / whoosh_duration, 0, 1)) ** 1.4
    whoosh = band_noise(rng, len(t), 140, 2_200) * whoosh_env
    add(whoosh, 3.78, 0.074, 0.28)
    add(whoosh[::-1], 3.86, 0.048, -0.36)

    # 0:03.88–0:06.55 — stereo cascade of tiny pearl impacts.
    impact_times = 3.84 + np.sort(rng.power(1.85, 58)) * 2.68
    for index, time in enumerate(impact_times):
        fade = 1.0 - 0.72 * ((time - 3.84) / 2.68)
        frequency = rng.uniform(2_100, 7_600)
        amplitude = rng.uniform(0.016, 0.052) * fade
        pan = rng.uniform(-0.92, 0.92)
        click(float(time), float(frequency), float(amplitude), float(pan), rng.uniform(0.010, 0.028))
        if index % 9 == 0:
            # Softer, lower skin/collar impacts.
            click(float(time + rng.uniform(0.015, 0.055)), rng.uniform(620, 1_150), amplitude * 0.72, pan * 0.6, 0.034)

    # 0:07.05–0:07.55 — one final isolated bounce and a smaller settling tick.
    click(7.08, 2_260, 0.075, -0.20, 0.045)
    click(7.34, 3_420, 0.035, 0.26, 0.031)

    # Gentle master limiting and fade to true silence.
    audio = np.tanh(audio * 1.08)
    peak = np.max(np.abs(audio)) or 1.0
    audio *= 0.94 / peak
    fade_start = int(7.52 * SAMPLE_RATE)
    audio[fade_start:] *= np.linspace(1.0, 0.0, sample_count - fade_start)[:, None]
    pcm = np.clip(audio * 32767, -32768, 32767).astype("<i2")

    output.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(output), "wb") as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(pcm.tobytes())


def make_video(audio_path: Path, output: Path) -> None:
    frames = [
        ROOT / "storyboard/frame_01_establishing_closeup.png",
        ROOT / "storyboard/frame_02_fingers_hooking.png",
        ROOT / "storyboard/frame_03_tension.png",
        ROOT / "storyboard/frame_04_snap.png",
        ROOT / "storyboard/frame_05_pearl_explosion.png",
        ROOT / "storyboard/frame_06_final_pearls_fall.png",
    ]
    durations = [2.20, 1.50, 0.75, 0.45, 2.35, 2.00]
    transitions = [0.45, 0.30, 0.08, 0.12, 0.30]
    starts = [0.0]
    for index in range(1, len(frames)):
        starts.append(starts[-1] + durations[index - 1] - transitions[index - 1])

    images = [Image.open(path).convert("RGB") for path in frames]
    output_size = (1080, 1920)
    zoom_ranges = [
        (1.010, 1.025),
        (1.025, 1.040),
        (1.040, 1.046),
        (1.046, 1.048),
        (1.048, 1.054),
        (1.050, 1.035),
    ]

    def visual_frame(index: int, local_time: float) -> Image.Image:
        image = images[index]
        progress = min(1.0, max(0.0, local_time / durations[index]))
        progress = progress * progress * (3.0 - 2.0 * progress)
        zoom_start, zoom_end = zoom_ranges[index]
        zoom = zoom_start + (zoom_end - zoom_start) * progress
        width, height = image.size
        target_ratio = output_size[0] / output_size[1]
        crop_width = min(float(width), float(height) * target_ratio) / zoom
        crop_height = crop_width / target_ratio
        center_x = width / 2.0
        center_y = height * 0.495
        box = (
            center_x - crop_width / 2,
            center_y - crop_height / 2,
            center_x + crop_width / 2,
            center_y + crop_height / 2,
        )
        return image.crop(box).resize(output_size, Image.Resampling.LANCZOS)

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    output.parent.mkdir(parents=True, exist_ok=True)
    command = [
        ffmpeg,
        "-y",
        "-loglevel", "error",
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "-s:v", f"{output_size[0]}x{output_size[1]}",
        "-r", str(FPS),
        "-i", "-",
        "-i", str(audio_path),
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-t", f"{DURATION:.3f}",
        "-vf", "eq=contrast=1.025:saturation=0.94:brightness=-0.008,noise=alls=1.0:allf=t,fade=t=in:st=0:d=0.16,fade=t=out:st=7.84:d=0.16",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-profile:v", "high",
        "-level", "4.2",
        "-pix_fmt", "yuv420p",
        "-r", str(FPS),
        "-color_primaries", "bt709",
        "-color_trc", "bt709",
        "-colorspace", "bt709",
        "-c:a", "aac",
        "-b:a", "256k",
        "-ar", str(SAMPLE_RATE),
        "-movflags", "+faststart",
        "-metadata", "title=THE NECKLACE SNAP",
        "-metadata", "comment=Luxury fashion film visualisation",
        str(output),
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    assert process.stdin is not None
    try:
        for frame_number in range(round(DURATION * FPS)):
            time = frame_number / FPS
            current = max(i for i, start in enumerate(starts) if start <= time)
            rendered = visual_frame(current, time - starts[current])

            if current > 0:
                transition = transitions[current - 1]
                blend_progress = (time - starts[current]) / transition
                if blend_progress < 1.0:
                    blend_progress = max(0.0, blend_progress)
                    blend_progress = blend_progress * blend_progress * (3.0 - 2.0 * blend_progress)
                    previous = visual_frame(current - 1, time - starts[current - 1])
                    rendered = Image.blend(previous, rendered, blend_progress)

            process.stdin.write(rendered.tobytes())
    finally:
        process.stdin.close()
    return_code = process.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, command)


if __name__ == "__main__":
    foley = ROOT / "sound/necklace_snap_foley.wav"
    video = ROOT / "output/the_necklace_snap.mp4"
    make_foley(foley)
    make_video(foley, video)
    print(video)
