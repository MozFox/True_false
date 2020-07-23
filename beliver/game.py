from typing import List, Tuple

from beliver.game_status import GameStatus


class Game:

    def __init__(self, allowed_mistakes: int = 3, file_path: str = ""):
        if 5 < allowed_mistakes < 0:
            raise ValueError("Number of allowed mistakes should be less than 5.")

        self.__file_path: str = file_path
        self.__allowed_mistakes = allowed_mistakes
        self.__game_status: GameStatus = GameStatus.IN_PROGRESS
        self.__counter: int = 0
        self.__mistakes: int = 0
        self.__quiz_ans_clar: List = []
        self.__player_answers: List = []

    def parse_line(self, line) -> Tuple:
        return tuple(line.split(';'))

    def open_file(self):
        with open(self.__file_path, encoding='utf-8') as file:
            for line in file:
                self.__quiz_ans_clar.append(self.parse_line(line))

    @property
    def game_status(self) -> GameStatus:
        return self.__game_status

    def get_next_question(self) -> str:
        return self.__quiz_ans_clar[self.__counter][0]

    def give_answer(self, answer: str):
        def is_last_question():
            return self.__counter == len(self.__quiz_ans_clar) - 1

        def exceeded_mistakes():
            return self.__mistakes > self.__allowed_mistakes

        def game_statistic():
            print(f'You answered {self.__player_answers.count("Right")} question(s)')
            for i, v in enumerate(self.__player_answers, 1):
                print(f"{i} - {v}")

        if self.__quiz_ans_clar[self.__counter][1] != answer:
            self.__mistakes += 1
            self.__player_answers.append("Mistake")
            print("Mistake!")
        else:
            self.__player_answers.append("Right")
            print("Right!")

        print(f"Clarification: {self.__quiz_ans_clar[self.__counter][2]}")

        if is_last_question():
            self.__game_status = GameStatus.GAME_OVER
            game_statistic()

        if exceeded_mistakes():
            self.__game_status = GameStatus.GAME_OVER
            print("You have used all the 'right to mistake'")
            game_statistic()

        self.__counter += 1


    def game(self):
        print("Game: True / False")
        self.open_file()
        while self.__game_status == GameStatus.IN_PROGRESS:
            print(self.get_next_question())
            answer = input("Give answer\n").lower()
            if answer in ["no", "n", "нет", "false"]:
                answer = "No"
            elif answer in ["yes", "y", "true", "да"]:
                answer = "Yes"
            else:
                raise ValueError("Incorrect answer. Please, answer Yes/No.")
            self.give_answer(answer)
