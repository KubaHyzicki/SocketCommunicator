#!/usr/bin/python3

import argparse

from modules.clientUI import ClientUI

def start_chat(client, args):
    client.start_chat()

def parse_arguments():
    parser = argparse.ArgumentParser()
    #ToDo: Add --debug arg
    #ToDo: Add --name [] arg
    #ToDo: Add --encryption_type [] arg

    subparser = parser.add_subparsers(
        title = 'method',
        dest = 'method'
    )
    subparser.required = True

    parser_start_chat = subparser.add_parser('start_chat')
    parser_start_chat.set_defaults(method = start_chat)

    return parser.parse_args()

def main():
    args = parse_arguments()

    clinet = ClientUI("Henio")
    clinet.set_up_connection()

    args.method(clinet, args)

if __name__ == "__main__":
    main()
