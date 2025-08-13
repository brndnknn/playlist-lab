from evaluator.models import Track, PlaylistInput, ScoreComponent, EvaluationResult
from pydantic import ValidationError
import pytest
import json

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
    sc = ScoreComponent(name="Prompt Alignment", value=7.5, max_value=10.0)
    assert sc.name == "Prompt Alignment"
    assert isinstance(sc.value, float)
    assert sc.value == 7.5
    assert sc.max_value == 10.0


def test_score_component_invalid_type():
    # test that passing non-floats for value or max_value raises a validation error
    with pytest.raises(ValidationError) as e1:
        ScoreComponent(name="Cohesion", value="abc", max_value=10.0)  # not coercible to float
    errs1 = e1.value.errors()
    assert any(err["loc"] == ("value",) for err in errs1)

    with pytest.raises(ValidationError) as e2:
        ScoreComponent(name="Humor", value=5.0, max_value="xyz")  # not coercible to float
    errs2 = e2.value.errors()
    assert any(err["loc"] == ("max_value",) for err in errs2)

# EvaluationResult 

def test_evaluation_result_creation():
    # test that an evaluation result can be created with 
    # prompt, score, score components, and track list
    tracks = [
        Track(title="Starman", artist="David Bowie"),
        Track(title="Life on Mars?", artist="David Bowie"),
    ]
    components = [
        ScoreComponent(name="Alignment", value=8.0, max_value=10.0),
        ScoreComponent(name="Cohesion", value=7.0, max_value=10.0),
        ScoreComponent(name="Humor", value=6.0, max_value=10.0),
    ]

    res = EvaluationResult(
        prompt="Darth Vader's tea party",
        overall_score=73.2,
        components=components,
        evaluated_tracks=tracks,
    )

    assert res.prompt.startswith("Darth Vader")
    assert isinstance(res.overall_score, float)
    assert len(res.components) == 3
    assert len(res.evaluated_tracks) == 2
    assert res.components[0].name == "Alignment"
    assert res.evaluated_tracks[0].title == "Starman"


def test_evaluation_result_invalid_score_component():
    # test that an invalid score component raises a validation error
    tracks = [Track(title="Starman", artist="David Bowie")]
    bad_components = [
        ScoreComponent(name="Alignment", value=8.0, max_value=10.0),
        123,  # invalid entry
    ]

    with pytest.raises(ValidationError) as e:
        EvaluationResult(
            prompt="Darth Vader's tea party",
            overall_score=70.0,
            components=bad_components,
            evaluated_tracks=tracks,
        )
    errs = e.value.errors()
    # Expect an error located under ("components", <index>)
    assert any(err["loc"][0] == "components" and isinstance(err["loc"][1], int) for err in errs)



def test_evaluation_result_invalid_track_list():
    # test that an invalid track in evaluated_tracks raises a validation error
    bad_tracks = [Track(title="Starman", artist="David Bowie"), 999]

    with pytest.raises(ValidationError) as e:
        EvaluationResult(
            prompt="Darth Vader's tea party",
            overall_score=70.0,
            components=[ScoreComponent(name="Alignment", value=8.0, max_value=10.0)],
            evaluated_tracks=bad_tracks,
        )
    errs = e.value.errors()
    # Expect an error located under ("evaluated_tracks", <index>)
    assert any(err["loc"][0] == "evaluated_tracks" and isinstance(err["loc"][1], int) for err in errs)



def test_evaluation_result_serialization_to_dict():
    # test that calling .dict() on an EvaluationResult returns a valid dictionary
    res = EvaluationResult(
        prompt="Darth Vader's tea party",
        overall_score=75.0,
        components=[ScoreComponent(name="Alignment", value=8.0, max_value=10.0)],
        evaluated_tracks=[Track(title="Starman", artist="David Bowie")],
    )
    as_dict = res.model_dump()
    assert isinstance(as_dict, dict)
    assert as_dict["prompt"] == "Darth Vader's tea party"
    assert isinstance(as_dict["components"], list)
    assert isinstance(as_dict["evaluated_tracks"], list)
    assert as_dict["components"][0]["name"] == "Alignment"
    assert as_dict["evaluated_tracks"][0]["artist"] == "David Bowie"


def test_evaluation_result_serialization_to_json():
    # test that calling .json() returns a valid JSON string
    res = EvaluationResult(
        prompt="Darth Vader's tea party",
        overall_score=75.0,
        components=[ScoreComponent(name="Alignment", value=8.0, max_value=10.0)],
        evaluated_tracks=[Track(title="Starman", artist="David Bowie")],
    )
    s = res.model_dump_json()  # <-- v2
    data = json.loads(s)
    assert isinstance(s, str)
    assert data["prompt"] == "Darth Vader's tea party"
    assert data["components"][0]["max_value"] == 10.0
    assert data["evaluated_tracks"][0]["title"] == "Starman"

