# https://docs.pytest.org/en/latest/

#RED > Green > Refactor

# $ postgres://bob:password@example.com:5432/db_one --driver s3 backups

import pytest
from pgbackup import cli

url = "postgres://bob:password@example.com:5432/db_one"

@pytest.fixture
def parser():
    return cli.create_parser()

def test_parser_without_driver(parser):
    """
    Without a specified driver the parser will exit
    """
    with pytest.raises(SystemExit):
       #parser = cli.create_parser()
        parser.parse_args([url])

def test_parser_with_driver():
    """
    The parser will exit if it receives a driver without a destination
    """
    parser = cli.create_parser()
    with pytest.raises(SystemExit):
        parser.parse_args([url, "--driver", "local"])

def test_parser_with_unknown_drivers():
    """
    The parser will exit if the driver name is unknown.
    """

    parser = cli.create_parser()
    with pytest.raises(SystemExit):
        parser.parse_args([url, "--driver", "azure", "destination"])

def test_parser_with_known_drivers():
    """
    The parser will not exit if the driver name is known
    """
    parser = cli.create_parser()
    for driver in ['local','s3']:
        assert parser.parse_args([url, '--driver', driver, 'destination'])


def test_parser_with_driver_and_destination():
    """
    Parser will not exit if it receives a driver and destination
    """
    parser = cli.create_parser()
    args = parser.parse_args([url, "--driver","local","/some/path"])
    assert args.url == url
    assert args.driver == "local"
    assert args.destination == "/some/path"




