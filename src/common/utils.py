"""Common utility functions"""

import random
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


def set_random_seed(seed: int) -> None:
    """Set random seed for reproducibility"""
    random.seed(seed)
    # If using numpy or torch, set their seeds too
    try:
        import numpy as np
        np.random.seed(seed)
    except ImportError:
        pass


def get_timestamp() -> str:
    """Get current timestamp as string"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def ensure_dir(path: Path) -> Path:
    """Ensure directory exists, create if not"""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_jsonl(file_path: str | Path) -> List[Dict[str, Any]]:
    """Load JSONL file"""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(json.loads(line))
    return data


def save_jsonl(data: List[Dict[str, Any]], file_path: str | Path) -> None:
    """Save data to JSONL file"""
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')


def append_jsonl(item: Dict[str, Any], file_path: str | Path) -> None:
    """Append a single item to JSONL file"""
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')


def load_json(file_path: str | Path) -> Dict[str, Any]:
    """Load JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: Dict[str, Any], file_path: str | Path, indent: int = 2) -> None:
    """Save data to JSON file"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=indent, default=str)
