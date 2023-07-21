from typing import Dict, Any
from gorest import users as client


# pylint: disable=unused-argument
def list_users_handler(event: Dict[str, Any], context: Any):
    page = None
    limit = None
    if event:
        page = event.get("page", 1)
        limit = event.get("limit", 10)
    return client.fetch_all(page, limit)


# pylint: disable=unused-argument
def read_user_handler(event: Dict[str, Any], context: Any):
    return client.fetch(event["id"])


def main():
    # pylint: disable=import-outside-toplevel
    import argparse
    import json
    import logging
    import os
    import sys

    # setup args
    parser = argparse.ArgumentParser(
        description="AWS Lambda command-line application for testing handlers."
    )
    parser.add_argument("lambda_handler", type=str, help="AWS Lambda hander name")
    parser.add_argument(
        "-e",
        "--event",
        type=str,
        help="AWS Event JSON object string or file path. For example: '{ \"id\": 1610 }'",
    )
    parser.add_argument(
        "-c",
        "--context",
        type=str,
        help="AWS Context JSON object string or file path. For example:"
        + ' \'{ "meta": "multiverse" }\'',
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (logging.DEBUG)",
    )
    args = parser.parse_args()

    # setup CLI logger
    loglevel = logging.WARNING
    if args.verbose != 0:
        loglevel = logging.DEBUG
    logging.basicConfig(level=loglevel, format="%(levelname)s: %(message)s")

    lambda_handler = args.lambda_handler
    event = None
    context = None

    # set event from arguement or file
    if args.event:
        try:
            event = json.loads(args.event)
            logging.debug("Parsed JSON event object: %s", event)
        except json.JSONDecodeError:
            if os.path.isfile(args.event):
                with open(args.event, "r", encoding="utf-8") as file:
                    event = json.load(file)
                    logging.debug("Loaded JSON event object from file: %s", event)

    logging.debug("lambda_handler=%s", lambda_handler)
    logging.debug("event=%s", event)
    logging.debug("context=%s", context)

    # check for and invoke lambda handler
    if hasattr(sys.modules[__name__], lambda_handler):
        result = getattr(sys.modules[__name__], lambda_handler)(event, context)
        print(json.dumps(result))
    else:
        logging.error(
            "No function named '%s' in this module (%s).", lambda_handler, __name__
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
