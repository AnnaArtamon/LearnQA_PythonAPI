
class TestFirstTestAPI:

    def test_insert_short_text(self):
        phrase = input("Set a phrase: ")
        length = len(phrase)
        assert length <= 15, "The phrase is longer than 15 symbols"