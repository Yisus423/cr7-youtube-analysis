import sys
from unittest.mock import MagicMock

# Mock dependencies before importing scripts.update_dataset
sys.modules["kaggle"] = MagicMock()
sys.modules["kaggle.api"] = MagicMock()
sys.modules["kaggle.api.kaggle_api_extended"] = MagicMock()
sys.modules["pandas"] = MagicMock()
sys.modules["scripts.preprocessing"] = MagicMock()

from scripts.update_dataset import get_file_hash, should_update

# Mock object for remote file metadata
class MockMetadata:
    def __init__(self, size):
        self.sizeInBytes = size

def test_get_file_hash(tmp_path):
    # Create a temporary file
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text("hello content")
    
    hash1 = get_file_hash(str(p))
    assert hash1 is not None
    assert isinstance(hash1, str)
    
    # Test non-existent file
    assert get_file_hash("non_existent.txt") is None

def test_should_update_no_local_file(tmp_path):
    local_path = tmp_path / "data.csv"
    metadata = MockMetadata(100)
    
    assert should_update(str(local_path), metadata) is True

def test_should_update_same_size(tmp_path):
    local_path = tmp_path / "data.csv"
    # Write 100 bytes
    local_path.write_bytes(b"a" * 100)
    metadata = MockMetadata(100)
    
    assert should_update(str(local_path), metadata) is False

def test_should_update_different_size(tmp_path):
    local_path = tmp_path / "data.csv"
    # Write 50 bytes
    local_path.write_bytes(b"a" * 50)
    metadata = MockMetadata(100)
    
    assert should_update(str(local_path), metadata) is True
