"""Load and save user-level Canvas connection profiles."""

import json
import os
import tempfile
from pathlib import Path


def get_profile_file():
    """Return the profile store path, allowing an override for testing."""
    override = os.environ.get("CANVAS_PROFILES_FILE")
    if override:
        return Path(override).expanduser()

    if os.name == "nt" and os.environ.get("APPDATA"):
        config_dir = Path(os.environ["APPDATA"])
    else:
        config_dir = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return config_dir / "canvas-scripts" / "profiles.json"


def load_profiles(profile_file=None):
    """Return all saved profiles keyed by their user-selected names."""
    path = Path(profile_file) if profile_file else get_profile_file()
    if not path.exists():
        return {}

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Could not read Canvas profiles from {path}: {exc}") from exc

    profiles = data.get("profiles", {}) if isinstance(data, dict) else {}
    if not isinstance(profiles, dict):
        raise ValueError(f"Invalid Canvas profile store: {path}")
    for name, profile in profiles.items():
        if not isinstance(name, str) or not isinstance(profile, dict):
            raise ValueError(f"Invalid Canvas profile store: {path}")
        if not isinstance(profile.get("api_url", ""), str):
            raise ValueError(f"Invalid API URL in Canvas profile '{name}': {path}")
        if not isinstance(profile.get("api_key", ""), str):
            raise ValueError(f"Invalid API key in Canvas profile '{name}': {path}")
    return profiles


def save_profile(name, api_url, api_key, profile_file=None):
    """Create or update one profile without discarding other profiles."""
    if not name.strip():
        raise ValueError("Profile name cannot be empty.")

    path = Path(profile_file) if profile_file else get_profile_file()
    profiles = load_profiles(path)
    profiles[name] = {"api_url": api_url.rstrip("/"), "api_key": api_key}
    payload = json.dumps({"version": 1, "profiles": profiles}, indent=2) + "\n"

    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=path.parent,
        prefix=".profiles-",
        delete=False,
    ) as temp_file:
        temp_file.write(payload)
        temp_path = Path(temp_file.name)

    if os.name != "nt":
        temp_path.chmod(0o600)
    temp_path.replace(path)
    return path


def load_canvas_profile(name):
    """Resolve a saved profile, with optional one-command environment overrides."""
    profile = load_profiles().get(name, {})
    api_url = os.environ.get("CANVAS_API_URL") or profile.get("api_url", "")
    api_key = os.environ.get("CANVAS_API_KEY") or profile.get("api_key", "")
    return api_url.rstrip("/"), api_key
