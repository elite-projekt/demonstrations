#!/usr/bin/env python3
"""Tool to manage demos in the portal with CRUD support."""

__version__ = "0.2"

import json
import re
import textwrap
import validators
import questionary
from questionary import Validator, ValidationError, Style, Choice


DEMOS_PATH = 'native/nativeapp/demos.json'
demos = {}
CreatingDemo = False
answers_update = {}

categories = {
    "phishing": "Phishing",
    "email": "Email",
    "password": "Passwords",
    "driveByDownload": "Drive-By Download",
    "ransomware": "Ransomware",
    "twoFactorAuthentication": "2-Factor-Authentification"
}

prompt_style = Style([
    ('qmark', 'fg:#ansired bold'),
    ('question', 'fg:#ansiyellow'),
    ('answer', 'fg:#ansiblue bold'),
    ('pointer', 'fg:#ansicyan bold'),
    ('selected', 'fg:#cc5454'),
    ('separator', 'fg:#cc5454'),
    ('disabled', 'fg:#858585 italic')
])


def iterate_all(iterable, returned="key"):
    """Returns an iterator that returns all keys or values
       of a (nested) iterable.

       Arguments:
           - iterable: <list> or <dictionary>
           - returned: <string> "key" or "value"
       Returns:
           - <iterator>
    """

    if isinstance(iterable, dict):
        for key, value in iterable.items():
            if returned == "key":
                yield key
            elif returned == "value":
                if not (isinstance(value, dict) or isinstance(value, list)):
                    yield value
            else:
                raise ValueError(
                    "'returned' keyword only accepts 'key' or 'value'.")
            for ret in iterate_all(value, returned=returned):
                yield ret
    elif isinstance(iterable, list):
        for el in iterable:
            for ret in iterate_all(el, returned=returned):
                yield ret


# load json files
with open(DEMOS_PATH, encoding='utf-8') as f_demos:
    data_demos = json.load(f_demos)

# parse demos to a dict for easier handling
demos = {demo['id']: demo for demo in data_demos}

# convert back to list of dicts
# list(demos.values())

locales_en = [x['messages']['en'] for x in data_demos]
locales_de = [x['messages']['de'] for x in data_demos]


# check if locales have each others keys
def validate_locales():
    all_keys_de = list(iterate_all(locales_de))
    all_keys_en = list(iterate_all(locales_en))
    if not (all_keys_de == all_keys_en):
        questionary.print(
                "There are invalid locales files!\n"
                "Check for same key existence of items in both languages:",
                style="bold italic fg:ansired")
        questionary.print("  location: {}".format(DEMOS_PATH),
                          style="fg:ansicyan")
        exit(18)


validate_locales()


class TimeValidator(Validator):
    def validate(self, document):
        min_val = 5
        max_val = 90
        message = 'Please enter a number from {}-{} and dividable ' \
                  'through 5 (10, 15, ...)'.format(str(min_val), str(max_val))
        try:
            number = int(document.text)
            # raise error if number is not dividable through 5
            # or if not in range (5-90)
            if bool(number % 5) or number < min_val or number > max_val:
                raise ValidationError(message=message,
                                      cursor_position=len(document.text))
        # raise error if input is not a number
        except ValueError:
            raise ValidationError(
                message=message,
                cursor_position=len(document.text)
            )


class DemoNameValidator(Validator):
    def validate(self, document):
        # raise error if demo is not matching the constraints
        if not re.match('^[a-z]+$', document.text):
            raise ValidationError(
                message='The name will be used as an id and therefore'
                        'lowercase only without special chars',
                cursor_position=len(document.text)
            )
        # raise error if demo exists
        if str(document.text) in list(demos.keys()):
            raise ValidationError(
                message='A demo with this name already exists.',
                cursor_position=len(document.text)
            )


class URLValidator(Validator):
    def validate(self, document):
        # raise error if URL is invalid
        if not validators.url(document.text):
            raise ValidationError(
                message='The URL seems invalid.'
                        'Check for typo or missing http(s)://',
                cursor_position=len(document.text)
            )


questions_new_demo = [
    {
        'type': 'input',
        'name': 'id',
        'message': 'Name of new demo:',
        'validate': DemoNameValidator
    }
]


def create_new_demo():
    try:
        global CreatingDemo, answers_update
        CreatingDemo = True
        answers_update['fieldToUpdate'] = ''
        answers_create = questionary.unsafe_prompt(questions_new_demo,
                                                   style=prompt_style)
        answers_create.update(questionary.unsafe_prompt(
            questions_general, style=prompt_style))

        locales_skeleton = {
            "title": str(answers_create['id']).capitalize(),
            "description": f"This demo shows {answers_create['id']} scenarios",
            "guide": [
                {
                    "title": "Briefing",
                    "content": ""
                },
                {
                    "title": "During Demo",
                    "content": ""
                },
                {
                    "title": "After Demo",
                    "content": ""
                },
            ]
        }

        demo_skeleton = {
            "id": "",
            "categories": [],
            "level": "",
            "status": 0,
            "time": 0,
            "secureMode": False,
            "disableSecureMode": True,
            "isRunning": False,
            "isAvailable": True,
            "messages": {
                "en": locales_skeleton,
                "de": locales_skeleton
            }
        }
        # portal: add demo to portal config file
        # remove unnecessary item before adding to demos
        demo_skeleton.update(answers_create)
        data_demos.append(demo_skeleton)
        write_json_to_file(data_demos, DEMOS_PATH)

        questionary.print("The demo has been added to the portal. You now can "
                          "specify the language specific contents (title, "
                          "description, guide) in the locales:",
                          style="bold italic fg:green")
        questionary.print("  file location: {}".format(DEMOS_PATH),
                          style="fg:blue")
    except KeyboardInterrupt:
        print("Cancelled by user")


def write_json_to_file(json_data: dict or list, file_path: str):
    with open(file_path, "w", encoding='utf-8') as outfile:
        json_obj = json.dumps(json_data, indent=4, ensure_ascii=False)
        outfile.write(json_obj)


# list available demos
def list_demos():
    questionary.print("{:<10} {:<55}".format(
            'Title', 'Description'),
            style="bold italic fg:ansiyellow")

    for demo in demos.keys():
        try:
            questionary.print("{:<10} {:<55}".format(
                demos[demo]['messages']['en']['title'], textwrap.shorten(
                    demos[demo]['messages']['en']['description'], width=55,
                    placeholder=" (...)")),
                style="bold fg:ansicyan")
        except KeyError:
            questionary.print("{:<10} {:<55}".format(
                str(demo).capitalize(),
                "Demo exists but has invalid locales files!"),
                style="bold italic fg:ansired")


questions_update_demo = [
    {
        'type': 'list',
        'name': 'demoToUpdate',
        'message': 'Which demo would you like update?',
        'choices': list(demos.keys())
    },
    {
        'type': 'checkbox',
        'name': 'fieldToUpdate',
        'message': 'Choose the parts you want to update',
        'choices': [
            {'name': 'categories'},
            {'name': 'level'},
            {'name': 'time'},
            {'name': 'disableSecureMode'},
            ],
    }
]

questions_general = [
    {
        'type': 'checkbox',
        'name': 'categories',
        'message': 'Choose the categories',
        'choices': categories.keys(),
        'when': lambda _:
            CreatingDemo or 'categories' in answers_update['fieldToUpdate']
    },
    {
        'type': 'list',
        'name': 'level',
        'message': 'Choose level of demo:',
        'default': 'beginner',
        'choices': [
            'beginner', 'intermediate'
        ],
        'when': lambda _:
            CreatingDemo or 'level' in answers_update['fieldToUpdate']
    },
    {
        'type': 'input',
        'name': 'time',
        'message': 'Estimate the time duration in rounded minutes:',
        'validate': TimeValidator,
        'filter': lambda val: int (val),
        'when': lambda _:
            CreatingDemo or 'time' in answers_update['fieldToUpdate']
    },
    {
        'type': 'confirm',
        'message': 'Does the demo have a secure mode?',
        'name': 'disableSecureMode',
        'default': True,
        'filter': lambda val: not(val),
        'when': lambda _:
            CreatingDemo
            or 'disableSecureMode' in answers_update['fieldToUpdate']
    }
]


def update_demo():
    global CreatingDemo, answers_update
    CreatingDemo = False
    try:
        answers_update = questionary.unsafe_prompt(
            questions_update_demo, style=prompt_style)
        answers_update.update(questionary.unsafe_prompt(
            questions_general, style=prompt_style))

        for field in answers_update["fieldToUpdate"]:
            demo_id = answers_update["demoToUpdate"]
            demos[demo_id][field] = answers_update[field]
        data_demos = list(demos.values())
        write_json_to_file(data_demos, DEMOS_PATH)

        questionary.print("The demo has been successfully updated",
                          style="bold italic fg:green")
    except KeyboardInterrupt:
        print("Cancelled by user")


def delete_demo():
    custom_style = questionary.Style([("question", "fg:#ansired bold")])
    answers_delete = questionary.form(
        demoToDelete=questionary.select("Which demo would you like delete?",
                                        choices=list(demos.keys())),
        confirm=questionary.confirm("Are you really sure?", default=False,
                                    style=custom_style),
        ).ask()
    if len(answers_delete) == 0 or not answers_delete['confirm']:
        return

    # portal: remove demo from portal config
    demos.pop(answers_delete['demoToDelete'])
    data_demos = list(demos.values())
    write_json_to_file(data_demos, DEMOS_PATH)

    questionary.print("The demo has been successfully updated",
                      style="bold italic fg:#ansigreen")


if __name__ == "__main__":
    try:
        crud_cmd = questionary.select("What do you want to do?", choices=[
            Choice("Add a demo", value="create"),
            Choice("Show all existing demos", value="read"),
            Choice("Update an existing demo", value="update"),
            Choice("Remove a demo", value="delete"),
        ], style=prompt_style, ).unsafe_ask()

        crud_commands = {
            "create": create_new_demo,
            "read": list_demos,
            "update": update_demo,
            "delete": delete_demo,
        }

        crud_commands[crud_cmd]()
    except KeyboardInterrupt:
        print("Cancelled by user")
