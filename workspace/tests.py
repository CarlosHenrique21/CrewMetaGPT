import unittest
from unittest.mock import patch, mock_open
import os
from src.snake import Snake
from src.food import Food
from src.score import Score
from src.game import Game
from src.config import GRID_WIDTH, GRID_HEIGHT

class TestSnake(unittest.TestCase):
    def setUp(self):
        self.snake = Snake([(5,5), (4,5), (3,5)])

    def test_initial_head_position(self):
        self.assertEqual(self.snake.get_head_position(), (5,5))

    def test_turn_valid_and_reverse(self):
        self.snake.turn((0, -1))  # turn up
        self.assertEqual(self.snake.direction, (0, -1))
        self.snake.turn((0, 1))  # attempt reverse down - should ignore
        self.assertEqual(self.snake.direction, (0, -1))

    def test_move_without_growth(self):
        initial_length = len(self.snake.positions)
        head_before = self.snake.get_head_position()
        self.snake.move()
        head_after = self.snake.get_head_position()
        self.assertEqual(len(self.snake.positions), initial_length)
        self.assertNotEqual(head_before, head_after)

    def test_grow(self):
        self.snake.grow()
        initial_length = len(self.snake.positions)
        self.snake.move()
        self.assertEqual(len(self.snake.positions), initial_length + 1)

    def test_self_collision_check(self):
        # Create collision by positions
        self.snake.positions = [(2,2), (2,3), (3,3), (3,2), (2,2)]
        self.assertTrue(self.snake.check_self_collision())

class TestFood(unittest.TestCase):
    @patch('random.choice')
    def test_spawn_food_free_space(self, mock_choice):
        snake_positions = [(0, 0), (1, 0)]
        available_positions = [(x, y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT) if (x,y) not in snake_positions]
        mock_choice.side_effect = lambda x: x[0]
        food = Food(snake_positions)
        self.assertIn(food.position, available_positions)

    def test_spawn_no_space(self):
        # All positions are taken
        snake_positions = [(x, y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)]
        food = Food(snake_positions)
        self.assertIsNone(food.position)

class TestScore(unittest.TestCase):
    def test_increase_and_reset(self):
        score = Score()
        score.increase(3)
        self.assertEqual(score.current_score, 3)
        score.reset()
        self.assertEqual(score.current_score, 0)

    @patch('builtins.open', new_callable=mock_open, read_data='{"high_score": 10}')
    def test_load_high_score_valid(self, mock_file):
        score = Score()
        score.load_high_score()
        self.assertEqual(score.high_score, 10)

    @patch('builtins.open', new_callable=mock_open)
    def test_save_high_score(self, mock_file):
        score = Score()
        score.high_score = 5
        score.current_score = 10
        score.save_high_score()
        mock_file.assert_called_once_with('highscore.json', 'w')

    @patch('builtins.open', side_effect=IOError)
    def test_save_high_score_ioerror(self, mock_file):
        score = Score()
        score.high_score = 0
        score.current_score = 10
        # Should handle IOError gracefully
        try:
            score.save_high_score()
        except Exception:
            self.fail("save_high_score raised exception unexpectedly")

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_initial_state(self):
        self.assertFalse(self.game.is_game_over())
        self.assertGreater(len(self.game.get_snake_positions()), 0)
        self.assertIsNotNone(self.game.get_food_position())

    def test_game_update_moves_snake(self):
        head_before = self.game.get_snake_positions()[0]
        self.game.update(None)  # move forward
        head_after = self.game.get_snake_positions()[0]
        self.assertNotEqual(head_before, head_after)

    def test_boundary_collision_sets_game_over(self):
        # Move snake head outside boundaries manually
        self.game.snake.positions[0] = (GRID_WIDTH, GRID_HEIGHT)
        self.game.update(None)
        self.assertTrue(self.game.is_game_over())

    def test_self_collision_sets_game_over(self):
        self.game.snake.positions = [(5,5), (5,6), (6,6), (6,5), (5,5)]
        self.game.update(None)
        self.assertTrue(self.game.is_game_over())

    def test_eating_food_increases_score_and_grows(self):
        head = self.game.get_snake_positions()[0]
        self.game.food.position = head  # place food on head (simulate eating)
        score_before = self.game.get_score()
        length_before = len(self.game.get_snake_positions())
        self.game.update(None)
        self.assertEqual(self.game.get_score(), score_before + 1)
        self.assertGreater(len(self.game.get_snake_positions()), length_before)

    def test_reset(self):
        self.game.game_over = True
        self.game.score.increase(5)
        self.game.reset()
        self.assertFalse(self.game.is_game_over())
        self.assertEqual(self.game.get_score(), 0)


if __name__ == '__main__':
    unittest.main()
