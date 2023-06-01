from engine_classes import HH_api, Superjob_api
from utils import sorting, get_top, get_hh_vacancies_list, get_sj_vacancies_list


def main():
    keyword = input("Введите ключевое слово для поиска ваканскии:")

    hh_engine = HH_api(keyword)
    sj_engine = Superjob_api(keyword)

    hh_connector = hh_engine.get_json_connector("parsed_data/hh_vacancies.json")
    sj_connector = sj_engine.get_json_connector("parsed_data/sj_vacancies.json")
    for page in range(1):
        hh_vacancies = hh_engine.get_requests().json()["items"]
        for vacancy in hh_vacancies:
            hh_connector.insert(vacancy)

        sj_vacancies = sj_engine.get_requests().json()["objects"]
        for vacancy in sj_vacancies:
            sj_connector.insert(vacancy)

    while True:
        command = input("Введите команду(sort или top): ")
        if command == "sort":
            hh_vacancies = get_hh_vacancies_list(hh_connector)
            sj_vacancies = get_sj_vacancies_list(sj_connector)

            sorted_vacancies = sorting(hh_vacancies + sj_vacancies)

            for vacancy in sorted_vacancies:
                print(vacancy)
        elif command == "top":
            hh_vacancies = get_hh_vacancies_list(hh_connector)
            sj_vacancies = get_sj_vacancies_list(sj_connector)

            all_vacancies = hh_vacancies + sj_vacancies

            top_count = int(input("Введите количество вакансий для вывода:"))

            top_vacancies = get_top(all_vacancies, top_count)
            for vacancy in top_vacancies:
                print(vacancy)
        else:
            print("Некорректная команда. Попробуйте еще раз")
        continue_running = input("Хотите продолжить работу (y/n):")

        if continue_running.lower() == "n":
            hh_connector.clear_data()
            sj_connector.clear_data()

            break


if __name__ == "__main__":
    main()
