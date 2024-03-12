from habit import Habit
from db import get_db


class Testing:

    def setup_method:
        self.db = get_db("test.db")
    def test_habit:
        pass

    def teardown method:
        import os
        os.remove("test.db")