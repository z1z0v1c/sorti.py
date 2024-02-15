import os
from pathlib import Path
import sys
import tempfile
import pytest
from sorti import validate_args, change_dir, make_dir


@pytest.mark.parametrize("args", [["sorti.py", "source_dir", "dest_dir"]])
def test_validate_args_correct_args(args: list[str], mocker):
    mocker.patch.object(sys, "argv", args)
    validate_args()
    
    
@pytest.mark.parametrize("args", [["sorti.py", "source_dir"]])
def test_validate_args_incorrect_args(args: list[str], mocker):
    mocker.patch.object(sys, "argv", args)
    with pytest.raises(SystemExit) as exc_info:
        validate_args()
    assert exc_info.value.code == 1
    
    
def test_change_dir_correct_dir():
    with tempfile.TemporaryDirectory() as temp_dir:
        original_dir = os.getcwd()
        change_dir(temp_dir)
        # Assert change within temp dir
        assert os.getcwd() == temp_dir
        # Clean up and return to original dir
        os.chdir(original_dir)

        
def test_change_dir_wrong_dir():
    with pytest.raises(SystemExit) as exc_info:
        change_dir("wrong_path")
    # Assert sys.exit(1)
    assert exc_info.value.code == 1
    
    
def test_make_dir_not_existing():
    original_dir = os.getcwd()
    new_dir = Path(original_dir + "/new/dir")
    make_dir(new_dir)
    change_dir(new_dir)
    assert Path(os.getcwd()) == new_dir
    change_dir(original_dir)
    os.rmdir(new_dir)
