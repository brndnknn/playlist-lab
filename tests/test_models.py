from evaluator.models import Track, PlaylistInput, ScoreComponent, EvaluationResult
from pydantic import ValidationError
import pytest

# Track

def test_track_creation():
    # test that a track data object can be created with title and artist attributes 
     track = Track(title="Song Title", artist="Artist Name")
     assert track.title == "Song Title"
     assert track.artist == "Artist Name"


def test_track_invalid_type():
    # test that values of incorrect type raise validation error
    with pytest.raises(ValueError):
        Track(title=123, artist="Queen")


# PlaylistInput 

def test_playlist_input_creation():
    # test that playlist can be created with a prompt and a list of Track objects
    tracks = [Track(title="Imagine", artist="John Lennon")]
    playlist = PlaylistInput(prompt="Songs for peace", tracks=tracks)
    assert playlist.prompt == "Songs for peace"
    assert isinstance(playlist.tracks, list)
    assert len(playlist.tracks) == 1
    assert playlist.tracks[0].title == "Imagine"
    assert playlist.tracks[0].artist == "John Lennon"


def test_playlist_input_requires_prompt():
    # test that missing prompt raises a validation error
    tracks = [Track(title="Bicycle Race", artist="Queen")]
    with pytest.raises(ValidationError) as e:
        PlaylistInput(tracks=tracks) # no prompt provided
    errs = e.value.errors()
    assert any(err["loc"] == ("prompt",) and err["type"] == "missing" for err in errs)

def test_playlist_input_requires_track_list():
    # test that missing or null track list raises a validation error
    with pytest.raises(ValidationError) as e:
        PlaylistInput(prompt="Silent disco", tracks=None)
    errs = e.value.errors()
    assert any(err["loc"] == ("tracks",) and err["type"] == "list_type" for err in errs)

def test_playlist_input_with_invalid_track():
    # test that a playlist with a non-Track object in the track list raises a validation erro
    bad_tracks = [{"title": "Hey Jude", "artist": "The Beatles"}, 123]
    with pytest.raises(ValidationError) as e:
        PlaylistInput(prompt="Beatles greatest", tracks=bad_tracks)
    errs = e.value.errors()
    # Expect errors for each invalid item in the list (index 1 for the int, maybe index 0 if dict isn't a Track)
    assert any(err["loc"][0] == "tracks" and isinstance(err["loc"][1], int) for err in errs)

# ScoreComponent

def test_score_component_creation():
    # test that a score component can be created with name, value, and max_value
    pytest.fail("Not implemented yet")


def test_score_component_invalid_type():
    # test that passing non-floats for value or max_value raises a validation error
    pytest.fail("Not implemented yet")


# EvaluationResult 

def test_evaluation_result_creation():
    # test that an evaluation result can be created with 
    # prompt, score, score components, and track list
    pytest.fail("Not implemented yet")


def test_evaluation_result_invalid_score_component():
    # test that an invalid score component raises a validation error
    pytest.fail("Not implemented yet")


def test_evaluation_result_invalid_track_list():
    # test that an invalid track in evaluated_tracks raises a validation error
    pytest.fail("Not implemented yet")


def test_evaluation_result_serialization_to_dict():
    # test that calling .dict() on an EvaluationResult returns a valid dictionary
    pytest.fail("Not implemented yet")


def test_evaluation_result_serialization_to_json():
    # test that calling .json() returns a valid JSON string
    pytest.fail("Not implemented yet")

