import json
import os
import requests
from abc import ABC, abstractmethod


class Vacancy(ABC):

    @abstractmethod
    def vac_api(self):
        pass


class HeadHunterAPI(Vacancy):

    url = "https://api.hh.ru/vacancies"

    def vac_api(self):
        vac_api = requests.get(url=self.url, headers={"User-Agent": "Ru.Zubayr@gmail.com"})
        return vac_api.json()


class SuperJobApi(Vacancy):
    url = "https://api.superjob.ru/2.0/vacancies/"
    sp_api = os.environ.get('SuperJobAPI')

    def vac_api(self):
        get_api = requests.get(url=self.url, headers={'X-Api-App-Id': self.sp_api})
        return get_api.json()


class GetVacancy(ABC):

    def __init__(self, api):
        self.api = api
        self.name = None
        self.salary = None
        self.salary_from = None
        self.salary_to = None
        self.url = None
        self.address = None
        self.prof_rolles = None
        self.work_day = None

    @abstractmethod
    def get_vacancy(self):
        pass


class VacancyHH(GetVacancy):

    def __init__(self, api):
        super().__init__(api)

    def get_vacancy(self):
        list_item = []
        for item in self.api['items']:
            self.name = item['name']
            self.salary = item['salary']
            self.url = item['url']
            if item['salary'] is not None:
                if item['salary']['from'] is None:
                    self.salary_from = "Зп не указана"
                else:
                    self.salary_from = item['salary']['from']
                if item['salary']['to'] is None:
                    self.salary_to = "Зп не указана"
                else:
                    self.salary_to = item['salary']['to']
            if item['address'] is None:
                self.address = "Адрес не указан"
            else:
                self.address = item['address']['raw']
            self.prof_rolles = item['professional_roles'][0]['name']
            self.work_day = item['employment']['name']
            dict_item = {
                "name": self.name,
                "salary": self.salary,
                "url": self.url,
                "salary_from": self.salary_from,
                "salary_to": self.salary_to,
                "address": self.address,
                "prof_rolles": self.prof_rolles,
                "work_day": self.work_day
            }
            list_item.append(dict_item)
        return list_item

    def __lt__(self, other):
        if not isinstance(other, VacancySJ):
            raise TypeError("Неправильный ввод")
        return f"{self.salary} меньше {other.salary}"

    def __eq__(self, other):
        if not isinstance(other, VacancySJ):
            raise TypeError("Неправильный ввод")
        return f"{self.salary} равно {other.salary}"

    def __gt__(self, other):
        if not isinstance(other, VacancySJ):
            raise TypeError("Неправильный ввод")
        return f"{self.salary} больше {other.salary}"


class VacancySJ(GetVacancy):

    def __init__(self, api):
        super().__init__(api)

    def get_vacancy(self):
        list_item = []
        for item in self.api['objects']:
            self.name = item['profession']
            self.salary_from = item['payment_from']
            if item['payment_from'] is not None:
                if item['payment_from'] == 0:
                    self.salary_from = "Зп не указана"
                else:
                    self.salary_from = item['payment_from']
            if item['payment_to'] == 0:
                self.salary_to = "Зп не указана"
            else:
                self.salary_to = item['payment_to']
            if self.address is None:
                self.address = "Город не указан"
            else:
                self.address = item['town']['title']
            self.prof_rolles = item['catalogues'][0]['title']
            self.work_day = item['type_of_work']['title']
            dict_item = {
                "name": self.name,
                "salary": self.salary,
                "url": self.url,
                "salary_from": self.salary_from,
                "salary_to": self.salary_to,
                "address": self.address,
                "prof_rolles": self.prof_rolles,
                "work_day": self.work_day
            }
            list_item.append(dict_item)
        return list_item

    def __lt__(self, other):
        if not isinstance(other, VacancyHH):
            raise TypeError("Неправильный ввод")
        return f"{self.salary} меньше {other.salary}"

    def __eq__(self, other):
        if not isinstance(other, VacancySJ):
            raise TypeError("Неправильный ввод")
        return f"{self.salary} равно {other.salary}"

    def __gt__(self, other):
        if not isinstance(other, VacancySJ):
            raise TypeError("Неправильный ввод")
        return f"{self.salary} больше {other.salary}"


class AbstractJsonSaver(ABC):

    @abstractmethod
    def add_vacancy(self, vacancy_data):
        pass

    @abstractmethod
    def get_data(self, get_vacancy):
        pass

    @abstractmethod
    def del_vacancy(self, vacancy_id):
        pass


class JsonSaver(AbstractJsonSaver):

    def __init__(self, path):
        self.path = path

    def add_vacancy(self, vacancy_data):
        with open(self.path, 'r') as file:
            vacancies = json.load(file)
            vacancies.append(vacancy_data)
        with open(self.path, 'w') as file:
            json.dump(vacancies, file, indent=4)

    def get_data(self, get_vacancy):
        with open(self.path, 'r') as file:
            vacancies = json.load(file)
            filtered_vacancies = []
            for vacancy in vacancies:
                if all(vacancy.get(key) == value for key, value in get_vacancy.items()):
                    filtered_vacancies.append(vacancy)

    def del_vacancy(self, vacancy_id):
        with open(self.path, 'r') as file:
            vacancies = json.load(file)
            for vacancy in vacancies:
                if vacancy['vacancy_id'] == vacancy_id:
                    vacancies.remove(vacancy)
                    break
        with open(self.path, 'w') as file:
            json.dump(vacancies, file, indent=4)


# hh = HeadHunterAPI()
# lt = hh.vac_api()
# lt2 = VacancyHH(lt)
sj = SuperJobApi()
Super = sj.vac_api()
sjob = VacancySJ(Super)
print(sjob.get_vacancy())
#
# sp_api = os.environ.get('SuperJobApi')
# print(sp_api)
