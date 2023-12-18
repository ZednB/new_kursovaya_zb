import json
import os
import requests
from abc import ABC, abstractmethod


class Vacancy(ABC):

    @abstractmethod
    def vac_api(self, name):
        pass


class HeadHunterAPI(Vacancy):

    url = "https://api.hh.ru/vacancies"

    def vac_api(self, name):
        vac_api = requests.get(url=self.url, headers={"User-Agent": "Ru.Zubayr@gmail.com"},
                               params={'text': name, 'page': None, 'per_page': 10})
        return vac_api.json()


class SuperJobAPI(Vacancy):
    url = "https://api.superjob.ru/2.0/vacancies/"
    sp_api = os.environ.get('SuperJobAPI')

    def vac_api(self, name):
        get_api = requests.get(url=self.url, headers={'X-Api-App-Id': self.sp_api},
                               params={'keyword': name, 'page': None, 'per_page': 10})
        return get_api.json()


class GetVacancy(ABC):

    def __init__(self, api):
        self.api = api
        self.name = None
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
            if self.url is None:
                self.url = "Ссылка не указана"
            else:
                self.url = item['url']
            if item['salary'] is not None:
                if item['salary']['from'] is None:
                    self.salary_from = 0
                else:
                    self.salary_from = item['salary']['from']
                if item['salary']['to'] is None:
                    self.salary_to = 0
                else:
                    self.salary_to = item['salary']['to']
            if item['address'] is None or 'null':
                self.address = "Адрес не указан"
            else:
                self.address = item['address']['raw']
            self.prof_rolles = item['professional_roles'][0]['name']
            self.work_day = item['employment']['name']
            dict_item = {
                "name": self.name,
                "url": self.url,
                "salary_from": self.salary_from,
                "salary_to": self.salary_to,
                "address": self.address,
                "prof_rolles": self.prof_rolles,
                "work_day": self.work_day
            }
            list_item.append(dict_item)
        return list_item


class VacancySJ(GetVacancy):

    def __init__(self, api):
        super().__init__(api)

    def get_vacancy(self):
        list_item = []
        for item in self.api['objects']:
            self.name = item['profession']
            if self.url is None:
                self.url = "Ссылка не указана"
            else:
                self.url = item['link']
            if item['payment_from'] is not None:
                if item['payment_from'] == 0:
                    self.salary_from = 0
                else:
                    self.salary_from = item['payment_from']
            if item['payment_to'] == 0:
                self.salary_to = 0
            else:
                self.salary_to = item['payment_to']
            if self.address is None or 'null':
                self.address = "Город не указан"
            else:
                self.address = item['address']
            if item['catalogues'][0]['title'] is not None:
                self.prof_rolles = item['catalogues'][0]['title']
            else:
                self.prof_rolles = "Не указано"
            self.work_day = item['type_of_work']['title']
            dict_item = {
                "name": self.name,
                "url": self.url,
                "salary_from": self.salary_from,
                "salary_to": self.salary_to,
                "address": self.address,
                "prof_rolles": self.prof_rolles,
                "work_day": self.work_day
            }
            list_item.append(dict_item)
        return list_item


def get_vacancies():
    with open('saver.json', 'r') as file:
        vacancies = json.load(file)
    return vacancies


def delete_vacancy():
    os.remove('saver.json')


class JSONSaver:

    def __init__(self, hh, sj):
        self.hh = hh
        self.sj = sj

    def add_vacancy(self):
        with open("saver.json", 'w', encoding='utf-8') as file:
            json.dump({'vacancy_hh': self.hh,
                      'vacancy_sj': self.sj},
                      file, ensure_ascii=False, indent=4)

    def get_vacancies(self):
        with open('saver.json', 'r') as file:
            vacancies = json.load(file)
        return vacancies

    def delete_vacancy(self):
        os.remove('saver.json')


class FilterWords:

    def __init__(self, vacancies):
        self.vacancies = vacancies
        self.hh = self.vacancies['vacancy_hh']
        self.sj = self.vacancies['vacancy_sj']

    def filter_vacs_hh(self):
        list_1 = []
        dict_1 = []

        for i in self.hh:
            if i['salary_from'] and i['salary_to'] == 0:
                continue
            elif i['salary_from'] != 0:
                dict_1.append(i['salary_from'])
            elif i['salary_to'] != 0:
                dict_1.append(i['salary_to'])
        dict_1.sort(reverse=True)

        for o in dict_1:
            for i in self.hh:
                if o == i['salary_from']:
                    name_sal = f"{i['name']}, {i['salary_from']}"
                    list_1.append(name_sal)
                elif o == ['salary_to']:
                    name_sal = f"{i['name']}, {i['salary_to']}"
                    list_1.append(name_sal)
        return list_1

    def filter_vacs_sj(self):
        list_1 = []
        dict_1 = []

        for i in self.sj:
            if i['salary_from'] and i['salary_to'] == 0:
                continue
            elif i['salary_from'] != 0:
                dict_1.append(i['salary_from'])
            elif i['salary_to'] != 0:
                dict_1.append(i['salary_to'])
        dict_1.sort(reverse=True)

        for o in dict_1:
            for i in self.sj:
                if o == i['salary_from']:
                    name_sal = f"{i['name']}, {i['salary_from']}"
                    list_1.append(name_sal)
                elif o == ['salary_to']:
                    name_sal = f"{i['name']}, {i['url']}, {i['address']}, {i['work_day']}, {i['salary_to']}"
                    list_1.append(name_sal)
        return list_1


class FilterRolles:

    def __init__(self, vacancies):
        self.vacancies = vacancies
        self.hh = self.vacancies['vacancy_hh']
        self.sj = self.vacancies['vacancy_sj']

    def filter_rolles_hh(self):
        list_1 = []
        dict_1 = []

        for i in self.hh:
            if i['prof_rolles'] is None:
                continue
            elif i['prof_rolles'] is not None:
                dict_1.append(i['prof_rolles'])
        dict_1.sort(reverse=True)

        for o in dict_1:
            for i in self.hh:
                if o == i['prof_rolles']:
                    prof_words = f"{i['name']}, {i['url']}, {i['address']}, {i['work_day']}, {i['prof_rolles']}, {i['salary_from']}"
                    list_1.append(prof_words)

        return list_1

    def filter_rolles_sj(self):
        list_1 = []
        dict_1 = []

        for i in self.sj:
            if i['prof_rolles'] is None:
                continue
            elif i['prof_rolles'] is not None:
                dict_1.append(i['prof_rolles'])
        dict_1.sort(reverse=True)

        for o in dict_1:
            for i in self.sj:
                if o == i['prof_rolles']:
                    prof_words = f"{i['name']}, {i['url']}, {i['address']}, {i['work_day']}, {i['prof_rolles']}, {i['salary_from']}"
                    list_1.append(prof_words)
        return list_1
