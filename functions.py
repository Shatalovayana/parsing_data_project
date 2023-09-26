from API_manager import HHAPIManager, SJAPIManager
from file_manager import JSONFileManager


def choose_platform():
    """
    Функция для общения с пользователем (для выбора платформы)
    """
    print('Выберите платформу для поиска: ')
    print('1 - HeadHunter\n'
          '2 - SuperJob\n'
          '3 - HeadHunter and SuperJob\n')


def choose_vacancy():
    """
    Функция для получения вакансии для поиска
    """
    print('Выберите вакансию для поиска: ')
    user_input = input()
    return user_input


def get_vacancies(api_manager: list):
    """
    Функция для сбора вакансий по апи
    """
    vacancies = []
    for api in api_manager:
        vacancies.extend(api.format_data())
    return vacancies


def get_top_vacancies(file_manager, user_input_n):
    """
    Функция для получения отсортированных вакансий по зарплате
    """
    vacancy_list = file_manager.get_list_vacancies()
    print("")
    sorted_vacancies = sorted(vacancy_list, key=lambda el: el['salary_from'], reverse=True)[:user_input_n]
    return sorted_vacancies


def actions_with_vacancies(file_manager):
    """
    Функция, которая предлагает пользователю выбрать действие
    и получает ответы пользователя
    """
    print('Выберите действие, которое необходимо выполнить: ')
    print('1 - Получить топ N вакансий по зарплате\n'
          '2 - Получить вакансии с фильтрацией по зарплате\n'
          '3 - Удаление вакансии по критерию\n'
          '0 - Выйти из программы\n')
    while True:
        user_input = input()
        if user_input in ('1', '2', '3', '0'):
            if user_input == '1':
                print('Введите количество вакансий для вывода: ')
                user_input_n = int(input())
                top_n = get_top_vacancies(file_manager, user_input_n)
                for vac in top_n:
                    print(vac)
                break
            elif user_input == '2':
                salary_input = int(input("Введите желаемую минимальную зарплату: "))
                min_salary = file_manager.get_vacancies_by_keyword({'salary_input': salary_input})
                for vac in min_salary:
                    print(vac)
                break
            elif user_input == '3':
                low_salary_input = int(input("Введите критерий(минимальную зарплату) для удаления: "))
                file_manager.delete_vacancy(file_manager.get_vacancies_by_keyword(low_salary_input))
                print(f'Вакансии удалены из файла по критерию: {low_salary_input}')
                break
            else:
                print('Всего хорошего!')
                break
        else:
            print('Введите корректный запрос: ')


def user_interaction():
    """
    Функция для взаимодействия с пользователем
    """
    keyword = choose_vacancy()
    choose_platform()
    while True:
        user_input = input()
        api_list = []
        if user_input in ('1', '2', '3'):
            if user_input == '1':
                hh = HHAPIManager(keyword)
                api_list.append(hh)
                break
            elif user_input == '2':
                sj = SJAPIManager(keyword)
                api_list.append(sj)
                break
            else:
                hh = HHAPIManager(keyword)
                sj = SJAPIManager(keyword)
                api_list.append(hh)
                api_list.append(sj)
                break
        else:
            print('Введите корректный запрос: ')
    file_manager = JSONFileManager('json_file_vacancies.json')
    file_manager.write_file(get_vacancies(api_list))
    actions_with_vacancies(file_manager)
