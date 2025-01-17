from api_module.py_clasess.search_api import SearchApi


class ApiController:
    def __init__(self):
        self.api_instance = SearchApi()

    def execute(self):
        print("API: Starting...")
        try:
            self.api_instance.run()
        except Exception as e:
            print(f"Error while running the API: {e}")
