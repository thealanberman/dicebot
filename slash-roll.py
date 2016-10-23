'''
This function handles a Slack /roll command and returns a dice roll to the channel in which it was invoked.
'''

import json
import re
from random import randint
from urlparse import parse_qs
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def rollXdice(dice,sides):
    results = []
    for _ in range(dice):
        results.append(randint(1,sides))
    return results


def isSuccessful(total, difficulty):
    if (total > difficulty):
        return "SUCCESS"
    elif (total == difficulty):
        return "TIE"
    else:
        return "FAILURE"


# returns Slack message JSON object stating that format was invalid
def invalidFormat():
  return { "text":"Improper format. Please use [number of dice]d[sides]\n[ Option 1: vs (Difficulty) ] e.g. '/roll 3d6 vs 15'\n[Option 2: +/- (Bonus) ] e.g. '/roll 3d6 +2'"}


def main(text, user):
    # default to 2d6 if no arguments given
    if re.match("^\s*$", text):
        text = "2d6"

    z = re.match("(\d+)\s*d\s*(\d+)(\s*(vs|[-+])\s*(\d+))?", text)
    # "3d6 -1" Example z match groups
    #  | | ||
    #  | | ||>> group(5)
    #  | | |>> group(4)
    #  | |>> group(2)
    #  |>> group(1)

    try:
        dice = int(z.group(1))
        sides = int(z.group(2))
        difficulty = 0
        bonus = 0

        if z.group(4) == "vs":
            difficulty = int(z.group(5))

        if z.group(4) == "+":
            bonus = int(z.group(5))

        if z.group(4) == "-":
            bonus = 0 - int(z.group(5))


        myRoll = rollXdice(dice,sides)
        mySum = sum(myRoll) + bonus
        mySuccess = "RESULTS"

        if difficulty != 0:
            mySuccess = isSuccessful(mySum, difficulty)

        slack_message = "*%s!* @%s rolled %s and got _%s_ %s" % (mySuccess, user, text, mySum, myRoll)
        response = { "response_type": "in_channel", "text": slack_message, "username": "DiceBot", 'icon_emoji': ':game_die:' }

    except AttributeError:
        response = invalidFormat()

    return response


def lambda_handler(event, context):
    params = parse_qs(event['body'])
    user = params['user_name'][0]
    command = params['command'][0]
    channel = params['channel_name'][0]
    try:
        command_text = params['text'][0]
    except KeyError:
        command_text = "2d6"

    return respond(None, main(command_text, user))
