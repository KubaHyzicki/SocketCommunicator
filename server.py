#!/usr/bin/python3

import os

from modules.serverUI import ServerUI

def main():
    #ToDo: Add argparser
    server = ServerUI()
    server.start_server()

if __name__ == "__main__":
    main()
