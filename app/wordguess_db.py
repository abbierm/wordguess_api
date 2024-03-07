# wordle clone for python programs
# plays wordle with python wordle solvers
# Clone of wordguess, adding a database


from collections import Counter
from datetime import datetime, timezone, timedelta
from .models import User, Solver, Game
from pydantic import BaseModel, ConfigDict, ValidationError
from typing import List, Optional
from .words.words import words
from .words.correct import correct_words



class GuessFeedback(BaseModel):
    guess_number: int
    guess: str
    feedback: Optional[str] = None




class GameData(BaseModel):
    game_id: str
    username: str
    total_guesses: int
    offical_guesses: int
    correct_word: str
    status: bool = True
    result: Optional[str] = None
    guesses: Optional[List[GuessFeedback]] = None


def _choose_word():
    length = len(words)
    x = random.randint(0, length - 1)
    return words[x]


def _validate_guess(guess) -> bool:
    if guess in correct_words:
        return True
    return false


def _feedback(correct_word, guess):
    correct_letter_counts = dict(Counter(correct_word))
    feedback_list = [1, 2, 3, 4, 5]
    yellow_letters = []
    for index, letter in enumerate(guess):
        if correct_word[index] == letter:
            feedback_list[index] = "G"
            correct_letter_counts[letter] -= 1
        elif letter not in correct_word:
            feedback_list[index] = "B"
        else:
            yellow_letters.append((index, letter))
    for tup in yellow_letters:
        i, l = tup[0], tup[1]
        if correct_letter_counts[l] > 0:
            feedback_list[i] = "Y"
            correct_letter_counts[l] -= 1
        else:
            feedback_list[i] = "B" 
    return ''.join(feedback_list)



def create_game(user_id: int, solver_id: int) -> dict:
    new_word = _choose_word()
    
    new_game = Game(
        user_id = user_id,
        solver_id = solver_id,
        correct_word = new_word,
    )
    db.session.add(new_game)
    db.session.commit()
    new_game.get_token()
    payload = self.create_payload()
    return payload




def game_loop(game_id, guess:str):
    user_game = db.session.scalar(sa.select(Game).where(Game.id == game_id))
    if _validate_guess(guess) == False:
        return user_game.create_payload(message='Word not found in our dictionary.')
    feedback = _feedback(user_game.correct_word, guess)

    # TODO: Update Database
    user_game.update_game(guess, feedback)
    if user_game.status == False:
        return user_game.create_payload(include_correct=True)
    return user_game.create_payload()
    