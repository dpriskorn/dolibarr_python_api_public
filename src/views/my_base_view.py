from datetime import datetime

import config
from src.helpers.console import console
from src.helpers.enums import InputType
from src.models.basemodels.my_base_model import MyBaseModel


class MyBaseView(MyBaseModel):
    def ask_date(self, text: str = "") -> datetime:
        answer = input(f"Type in {text} date [ddmmyy, default=today]:")
        if not answer:
            date = datetime.now(tz=self.stockholm_timezone)
        else:
            if len(answer) == 4:
                # Default to current year
                answer = answer + datetime.now(tz=self.stockholm_timezone).strftime(
                    "%y"
                )
            date = datetime.strptime(answer, "%d%m%y").astimezone(
                tz=self.stockholm_timezone
            )
        # https://stackabuse.com/converting-strings-to-datetime-in-python/
        # https://www.programiz.com/python-programming/datetime/strftime
        return date

    @staticmethod
    def ask_int(text: str):
        answer = input(text + " [int]:")
        if answer:
            if answer == "":
                return 0
            else:
                return int(answer)
        else:
            return 0

    @staticmethod
    def ask_mandatory(
        text: str,
        input_type: InputType = InputType.STRING,
        unit: str = "no unit applicable",
    ):
        """Ask mandatory question
        Defaults to no unit and InputType.STRING"""
        while True:
            answer = input(
                f"{text}\nPlease type it in: [{unit}, mandatory]:",
            )
            if len(answer) > 0:
                if input_type == InputType.INTEGER:
                    if isinstance(int(answer), int):
                        return int(answer)
                elif input_type == InputType.FLOAT:
                    if isinstance(float(answer), float):
                        return float(answer)
                elif input_type == InputType.STRING:
                    return answer
                else:
                    raise ValueError("this should never be reached")

    @staticmethod
    def ask_yes_no_question(message: str, default_yes: bool = True):
        # https://www.quora.com/
        # I%E2%80%99m-new-to-Python-how-can-I-write-a-yes-no-question
        # this will loop forever
        while True:
            if default_yes:
                answer = input(message + " [Y/n]: ")
                if len(answer) == 0 or answer[0].lower() in ("y", "n"):
                    if len(answer) == 0:
                        # no input means yes
                        return True
                    else:
                        # the == operator just returns a boolean,
                        return answer[0].lower() == "y"
            else:
                answer = input(message + " [y/N]: ")
                if len(answer) == 0 or answer[0].lower() in ("y", "n"):
                    if len(answer) == 0:
                        # no input means no
                        return False
                    else:
                        # the == operator just returns a boolean,
                        return answer[0].lower() == "n"

    @staticmethod
    def press_enter_to_continue():
        if config.press_enter_to_continue:
            console.input("Press Enter to continue")
