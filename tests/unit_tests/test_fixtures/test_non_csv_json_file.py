# Very basic python file to test that the read function does not process non-csv/json files


class TestClass:
    def __init__(self):
        self.message = "This is not a CSV or JSON file"

    def display_message(self):
        print(self.message)


if __name__ == "__main__":
    test_instance = TestClass()
    test_instance.display_message()
