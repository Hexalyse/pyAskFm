# -*- coding: utf-8 -*-

import AskApi

if __name__ == "__main__":
    ask = AskApi.Ask("8aab1704e5e0ab3e", True)  # Put a random device id here
    ask.login("login", "password")
    # We just get and print the JSON data of inbox questions
    print ask.getQuestions("0")

