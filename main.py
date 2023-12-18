from utils import HeadHunterAPI, SuperJobAPI, VacancyHH, JSONSaver, VacancySJ, FilterWords, get_vacancies, FilterRolles


if __name__ == "__main__":

    while True:
        vac = input("Введите интересующую вакансию: \n")
        quest = int(input("Выберите, с какой платформы вы хотите получить информацию о доступных "
                          "вакансиях: \n1 - HeadHunter \n2 - SuperJob \n0 - Для выхода \n"))

        hh = HeadHunterAPI()
        hh1 = hh.vac_api(vac)
        hh2 = VacancyHH(hh1)
        hh3 = hh2.get_vacancy()

        sj = SuperJobAPI()
        sj1 = sj.vac_api(vac)
        sj2 = VacancySJ(sj1)
        sj3 = sj2.get_vacancy()

        saver = JSONSaver(hh3, sj3)
        saver.add_vacancy()

        if quest == 0:
            break

        elif quest == 1:
            quest_2 = int(input("Выберите тип поиска: \n"
                                "1 - По ключевым словам \n"
                                "2 - По зарплате \n"
                                "0 - Выход \n"))

            if quest_2 == 0:
                break

            elif quest_2 == 1:
                filter_vacs = FilterRolles(get_vacancies())
                print(". ".join(filter_vacs.filter_rolles_hh()))
                break

            elif quest_2 == 2:
                filter_sal = FilterWords(get_vacancies())
                print(". ".join(filter_sal.filter_vacs_hh()))
                break

        elif quest == 2:
            quest_2 = int(input("Выберите тип поиска: \n"
                                "1 - По ключевым словам \n"
                                "2 - По зарплате \n"
                                "0 - Выход \n"))
            if quest_2 == 0:
                break

            elif quest_2 == 1:
                filter_vacs = FilterRolles(get_vacancies())
                print(". ".join(filter_vacs.filter_rolles_sj()))
                break

            elif quest_2 == 2:
                filter_sal = FilterWords(get_vacancies())
                print(". ".join(filter_sal.filter_vacs_sj()))
                break
        saver.delete_vacancy()
