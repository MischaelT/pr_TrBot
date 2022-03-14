import json

from data.storage_managers.storage_manager import storage_Manager


class Json_manager(storage_Manager):

    def __init__(self) -> None:
        super().__init__()

    def push_data(self, data):

        self._validate(data)
        self._write(data)

    def _write(self, data):
        with open("vacancies.jsonlines", 'a', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)
            file.write('\n')

    def _read(self):
        pass
