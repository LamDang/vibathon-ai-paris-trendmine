#!/usr/bin/env python3
"""Generate ElevenLabs audio for a script's hook and key points."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any, Dict, List

import requests

try:
    from dotenv import load_dotenv
except ImportError as exc:
    raise ImportError(
        "python-dotenv is required. Install it with `pip install python-dotenv`."
    ) from exc


ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
DEFAULT_MODEL = "eleven_multilingual_v2"


def load_script_data(json_path: Path) -> Dict[str, Any]:
    with json_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def find_script(scripts: List[Dict[str, Any]], script_number: int) -> Dict[str, Any]:
    for script in scripts:
        if script.get("script_number") == script_number:
            return script
    raise ValueError(f"Script number {script_number} not found in JSON.")


def ensure_env(var_name: str, cli_value: str | None = None) -> str:
    value = cli_value or os.getenv(var_name)
    if not value:
        raise EnvironmentError(
            f"Missing required value for {var_name}. "
            "Set the environment variable or pass it via the CLI."
        )
    return value


def generate_audio(
    text: str,
    voice_id: str,
    api_key: str,
    output_file: Path,
    model_id: str,
) -> None:
    payload = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {"stability": 0.3, "similarity_boost": 0.75},
    }
    headers = {"xi-api-key": api_key, "Content-Type": "application/json"}

    response = requests.post(
        ELEVENLABS_API_URL.format(voice_id=voice_id),
        headers=headers,
        json=payload,
        stream=True,
        timeout=60,
    )
    response.raise_for_status()

    with output_file.open("wb") as audio_file:
        for chunk in response.iter_content(chunk_size=4096):
            if chunk:
                audio_file.write(chunk)


def create_audio_tracks(
    script: Dict[str, Any],
    output_dir: Path,
    voice_id: str,
    api_key: str,
    model_id: str,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    tasks: List[Dict[str, Any]] = []

    hook_text = script.get("hook", "").strip()
    if hook_text:
        tasks.append(
            {
                "label": "hook",
                "text": hook_text,
                "path": output_dir / "hook.mp3",
            }
        )

    key_points = script.get("key_points") or []
    for index, point in enumerate(key_points, start=1):
        point_text = point.strip()
        if not point_text:
            continue
        tasks.append(
            {
                "label": f"key point {index}",
                "text": point_text,
                "path": output_dir / f"keypoint_{index:02}.mp3",
            }
        )

    if not tasks:
        print("No hook or key points to process.")
        return

    print(f"Generating {len(tasks)} audio clips sequentially...")
    for task in tasks:
        print(f"Generating {task['label']} -> {task['path'].name}")
        generate_audio(
            task["text"],
            voice_id,
            api_key,
            task["path"],
            model_id,
        )
        print(f"Finished {task['label']} -> {task['path']}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate ElevenLabs audio for hook and key points."
    )
    parser.add_argument(
        "script_json",
        type=Path,
        help="Path to the generated script JSON file.",
    )
    parser.add_argument(
        "--script-number",
        type=int,
        default=1,
        help="Script number to process (default: 1).",
    )
    parser.add_argument(
        "--voice-id",
        type=str,
        default=None,
        help="ElevenLabs voice ID (defaults to ELEVENLABS_VOICE_ID env var).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("audio-generation/output"),
        help="Directory to store generated audio files.",
    )
    parser.add_argument(
        "--model-id",
        type=str,
        default=DEFAULT_MODEL,
        help=f"ElevenLabs model to use (default: {DEFAULT_MODEL}).",
    )
    return parser.parse_args()


def load_env_file() -> None:
    env_path = Path(__file__).with_name(".env")
    if env_path.exists():
        load_dotenv(env_path)


def main() -> None:
    args = parse_args()

    load_env_file()

    api_key = ensure_env("ELEVENLABS_API_KEY")
    voice_id = ensure_env("ELEVENLABS_VOICE_ID", args.voice_id)

    data = load_script_data(args.script_json)
    scripts = data.get("scripts")
    if not scripts:
        raise ValueError("No scripts found in the JSON file.")

    script = find_script(scripts, args.script_number)

    script_title = script.get("title", f"script_{args.script_number}")
    script_dir_name = "".join(
        char if char.isalnum() or char in ("-", "_") else "-" for char in script_title
    ).strip("-")
    destination = args.output_dir / script_dir_name

    create_audio_tracks(
        script,
        destination,
        voice_id,
        api_key,
        args.model_id,
    )
    print(f"Audio files stored in: {destination}")


if __name__ == "__main__":
    main()
