import sys
import pytest
from sorti import validate_args


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
