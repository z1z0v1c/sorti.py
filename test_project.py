import os
from pathlib import Path
import tempfile
import pytest
from project import change_dir, make_dir, sortify_files
    
    
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


def test_sortify_files_correct_dir():
    original_dir = os.getcwd()
    
    with tempfile.TemporaryDirectory() as source_dir:
        jpg_file = mock_file(source_dir, ".jpg")
        deb_file = mock_file(source_dir, ".deb")
        py_file = mock_file(source_dir, ".py")
        txt_file = mock_file(source_dir, ".txt")
        mp4_file = mock_file(source_dir, ".mp4")
        mp3_file = mock_file(source_dir, ".mp3")
        
        with tempfile.TemporaryDirectory() as dest_dir:
            sortify_files(Path(source_dir), Path(dest_dir), recursive=False, remove_duplicates=False)

            assert os.path.exists(f"{dest_dir}/Applications/{deb_file}")
            assert os.path.exists(f"{dest_dir}/Code/{py_file}")
            assert os.path.exists(f"{dest_dir}/Documents/{txt_file}")
            assert os.path.exists(f"{dest_dir}/Pictures/{jpg_file}")
            assert os.path.exists(f"{dest_dir}/Videos/{mp4_file}")
            assert os.path.exists(f"{dest_dir}/Music/{mp3_file}")
            
    os.chdir(original_dir)


def test_sortify_files_recursive_correct_dir():
    original_dir = os.getcwd()

    with tempfile.TemporaryDirectory() as source_dir:
        jpg_file = mock_file(source_dir, ".jpg")
        deb_file = mock_file(source_dir, ".deb")
        py_file = mock_file(source_dir, ".py")

        source_subdir = os.path.join(source_dir, 'source_subdir')
        os.makedirs(source_subdir)

        txt_file = mock_file(source_subdir, ".txt")
        mp4_file = mock_file(source_subdir, ".mp4")
        mp3_file = mock_file(source_subdir, ".mp3")

        with tempfile.TemporaryDirectory() as dest_dir:
            sortify_files(Path(source_dir), Path(dest_dir), recursive=True, remove_duplicates=False)

            assert os.path.exists(f"{dest_dir}/Applications/{deb_file}")
            assert os.path.exists(f"{dest_dir}/Code/{py_file}")
            assert os.path.exists(f"{dest_dir}/Documents/{txt_file}")
            assert os.path.exists(f"{dest_dir}/Pictures/{jpg_file}")
            assert os.path.exists(f"{dest_dir}/Videos/{mp4_file}")
            assert os.path.exists(f"{dest_dir}/Music/{mp3_file}")

    os.chdir(original_dir)


def mock_file(source_dir, extension):
    with tempfile.NamedTemporaryFile(dir=source_dir, suffix=extension, delete=False) as f:
        splitted_path = f.name.split('/')
        return splitted_path[len(splitted_path) - 1]
