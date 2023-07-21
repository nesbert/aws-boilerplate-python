from pathlib import Path
from typing import Any
from unittest import mock

import json
import logging
import pytest
import requests_mock

from _pytest.logging import LogCaptureFixture
from example import lambda_handler as lh

# sample data to be used for mocking
mock_fetch_all_data = [{"id": 1, "name": "test user"}]
mock_fetch_data = {"id": 1, "name": "test user"}


def test_list_users_handler():
    with requests_mock.Mocker() as mocker:
        # Mock the fetch_all function in the client
        mocker.get("https://gorest.co.in/public/v2/users", json=mock_fetch_all_data)
        event = {"page": 1, "limit": 10}
        context = {}
        result = lh.list_users_handler(event, context)
        assert result == mock_fetch_all_data

        # Test with empty event
        event = {}
        result = lh.list_users_handler(event, context)
        assert result == mock_fetch_all_data


def test_read_user_handler():
    with requests_mock.Mocker() as mocker:
        # Mock the fetch function in the client
        mocker.get("https://gorest.co.in/public/v2/users/1", json=mock_fetch_data)
        event = {"id": 1}
        context = {}
        result = lh.read_user_handler(event, context)
        assert result == mock_fetch_data


@mock.patch("argparse.ArgumentParser.parse_args")
def test_main_with_read_user_handler(mock_args: Any, capsys: Any):
    # Create a mock args object with the desired properties
    mock_args.return_value = mock.Mock(
        lambda_handler="read_user_handler",
        event='{"id": 1}',
        context=None,
        verbose=0,
    )

    # Call the function under test
    with mock.patch("example.lambda_handler.client.fetch") as mock_fetch:
        mock_fetch.return_value = mock_fetch_data
        lh.main()

        captured = capsys.readouterr()
        assert json.dumps(mock_fetch_data) + "\n" == captured.out

        # Assert that the handler function was called with the correct argument
        mock_fetch.assert_called_once_with(1)


@mock.patch("argparse.ArgumentParser.parse_args")
def test_main_with_list_users_handler(mock_args: Any, capsys: Any):
    # Create a mock args object with the desired properties
    mock_args.return_value = mock.Mock(
        lambda_handler="list_users_handler",
        event='{"page": 2, "limit": 20}',
        context=None,
        verbose=1,
    )

    # Call the function under test
    with mock.patch("example.lambda_handler.client.fetch_all") as mock_fetch_all:
        mock_fetch_all.return_value = mock_fetch_all_data
        lh.main()

        captured = capsys.readouterr()
        assert json.dumps(mock_fetch_all_data) + "\n" == captured.out

        # Assert that the handler function was called with the correct argument
        mock_fetch_all.assert_called_once_with(2, 20)


def test_main_no_arguments(capsys: Any):
    """
    Test running main with no command-line arguments.
    Should raise SystemExit with error message about missing required lambda_handler argument.
    """
    with pytest.raises(SystemExit):
        with mock.patch("sys.argv", ["lambda"]):
            lh.main()

    captured = capsys.readouterr()
    assert "the following arguments are required: lambda_handler" in captured.err


def test_main_with_unknown_handler(caplog: LogCaptureFixture):
    """
    Test running main with an unknown lambda_handler.
    Should exit with error message about missing function.
    """
    with pytest.raises(SystemExit):
        with mock.patch("sys.argv", ["lambda", "unknown_handler"]):
            lh.main()

    # Check that an error was logged
    for log in caplog.record_tuples:
        if log[1] == logging.ERROR:
            assert "No function named 'unknown_handler' in this module" in log[2]
            break
    else:
        assert False, "No ERROR log found"


def test_main_with_known_handler_and_no_event(capsys: Any):
    """
    Test running main with a known lambda_handler and no event.
    """
    with mock.patch("sys.argv", ["lambda", "list_users_handler"]):
        with mock.patch.object(
            lh, "list_users_handler", return_value=mock_fetch_all_data
        ) as mock_handler:
            lh.main()

            captured = capsys.readouterr()
            assert json.dumps(mock_fetch_all_data) + "\n" == captured.out

            mock_handler.assert_called_once_with(None, None)


def test_main_event_file(capsys: Any, tmp_path: Path):
    # Create a temporary JSON file
    event_file = tmp_path / "event.json"
    event_data = {"id": 12345}
    event_file.write_text(json.dumps(event_data))

    # Mock out sys.argv
    mock_args = ["lambda", "read_user_handler", "--event", str(event_file)]

    # Mock read_user_handler to assert it was called correctly
    mock_handler = mock.Mock(return_value=mock_fetch_data)

    with mock.patch("sys.argv", mock_args), mock.patch(
        "example.lambda_handler.read_user_handler",
        new=mock_handler,
    ):
        # Run main
        lh.main()

    captured = capsys.readouterr()
    assert json.dumps(mock_fetch_data) + "\n" == captured.out

    # Check that the handler was called with the correct event data
    mock_handler.assert_called_once_with(event_data, None)
