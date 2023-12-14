from utils import HeadHunterAPI, SuperJobAPI, VacancyHH, JSONSaver, VacancySJ, FilterWords

if __name__ == "__main__":
    vac = input("Введите вакансию")

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

    fil = FilterWords(saver.get_vacancies())
    print(fil.filter_vacs_sj())
