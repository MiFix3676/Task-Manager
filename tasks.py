import json

class Task:
    def __init__(self, name, done=False, priority="Обычный"):
        self.name = name
        self.done = done
        self.priority = priority

    def mark_task(self):
        self.done = True

    def set_priority(self, new_priority):
        self.priority = new_priority

def load_tasks():
    loaded_tasks = []

    try:
        with open("tasks.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        for task in data:
            task1 = Task(task["name"], task["done"], task["priority"])
            loaded_tasks.append(task1)

    except FileNotFoundError:
        pass
    return loaded_tasks

tasks = load_tasks()
#1
def add_task(tasks_list):
    new_task = input("\nДобавте задачу: ")
    new_task = Task(new_task)
    tasks_list.append(new_task)
    print("\nЗадача добавлена!")
#2
def show_tasks(tasks_list):
    if len(tasks_list) == 0:
        print("\nЗадач нету :<")
    else:
        for i, task in enumerate(tasks_list, 1):
            status = "[X]" if task.done else "[ ]"
            print(f"\n{i}. {task.name} {status} ({task.priority.capitalize()})")
#3
def save_tasks(tasks_list, verbose=True):
    data = []
    for task in tasks_list:
        data.append({
            "name": task.name,
            "done": task.done,
            "priority": task.priority
        })
    with open("tasks.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False , indent=2)
    if verbose:
        print("Задачи сохранены в файл. Пока!")
#4
def delete_tasks(tasks_list):
    if len(tasks_list) == 0:
        print("Список пуст!!")
    else:
        show_tasks(tasks_list)

        try:
            index = int(input("\nВыберити номер для удаления: ")) - 1
        except ValueError:
            print("\nЭто не номер бро")
            return

        if 0 <= index < len(tasks_list):
            del tasks_list[index]
            print("Задача удалена!")
        else:
            print("Не верный номер!")
#5
def mark_tasks_menu(tasks_list):
    if len(tasks_list) == 0:
        print("\nСписок пуст!")
        return
    else:
        show_tasks(tasks)

        try:
            task = int(input("\nВыбирите задачу: ")) - 1
        except ValueError:
            print("\nТебя попросили выбрать задачу чел")
            return

        if 0 <= task < len(tasks_list):
            tasks_list[task].mark_task()
            print("\nЗадача отмечена!")
        else:
            print("\nНеверный номер!")
#6
def change_priority(tasks_list):
    show_tasks(tasks_list)
    try:
        index = int(input("\nВыберите номер: ")) - 1
    except ValueError:
        print("\nЧел это не номер")
        return
    if 0 <= index < len(tasks_list):
        new_priority = input("\nВедиде приоритет: ").strip().lower()
        tasks_list[index].set_priority(new_priority)
    else:
        print("Не верный номер!")
#7
def edit_task(tasks_list):
    show_tasks(tasks_list)
    try:
        index = int(input("\nВыберити номер задачи: ")) - 1
    except ValueError:
        print("Может номер введешь?")
        return
    if 0 <= index < len(tasks_list):
        new_task = input("\nНапишите новое название для задачи: ")
        if not new_task:
            print("Вы не ввели нове название!")
            return
        tasks_list[index].name = new_task
        print("\nЗадача изменина")
#8
def show_stats(tasks_list):
    if len(tasks_list) == 0:
        print("\nЗадач нету :<")
        return

    total = len(tasks_list)
    done_count = 0
    for task in tasks_list:
        if task.done:
            done_count += 1

    done_total = total - done_count
    print(
        f"\nВсего задач: {total}"
        f"\nВыполнено: {done_count}"
        f"\nОсталось: {done_total}"
          )
#9
def sorting_task(tasks_list):
    print(
        "\n1. По алфавиту"
        "\n2. По статусу"
        "\n3. По приоритету"
        "\n4. Назад"
        )
    try:
        sorting = int(input("\nВведи число: "))
    except ValueError:
        print("\nЭто не число!")
        return

    if sorting == 1:
        new_sorting = sorted(tasks_list, key=lambda task: task.name)
        show_tasks(new_sorting)
        return

    elif sorting == 2:
        new_sorting = sorted(tasks_list, key=lambda task: task.done)
        show_tasks(new_sorting)
        return

    elif sorting == 3:
        priority_order = {"высокий":1, "обычный":2, "низкий":3}
        new_sorting = sorted(tasks_list, key=lambda task: priority_order[task.priority.lower()])
        show_tasks(new_sorting)

    elif sorting == 4:
        return

    else:
        print("Неверный выбор")
#10
def search_task(tasks_list):
    search_word = input("\nЧто ищите? >").lower()
    if not search_word:
        print("\nВы ничего не ввели!")
        return
    found = False
    for task in tasks_list:
        if search_word in task.name.lower():
            print(task.name)
            found = True
    if not found:
        print("Ничего не найдено :<")
#Меню
while True:
    print(
        "\n1. Добавить задачу"
        "\n2. Показать задачу"
        "\n3. Выйти и сохранить"
        "\n4. Удалить задачу"
        "\n5. Отметить выполненной"
        "\n6. Изменить приоритет"
        "\n7. Изменить задачу"
        "\n8. Статистика"
        "\n9. Сортировка"
        "\n10. Поиск"
)
    choice = input("Выбирите действие (1/2/3/4/5/6/7/8/9/10): ").strip()

    if choice == "1":
        add_task(tasks)
        save_tasks(tasks, verbose=False)

    elif choice == "2":
        show_tasks(tasks)

    elif choice == "3":
        save_tasks(tasks)
        break

    elif choice == "4":
        delete_tasks(tasks)
        save_tasks(tasks, verbose=False)

    elif choice == "5":
        mark_tasks_menu(tasks)
        save_tasks(tasks, verbose=False)

    elif choice == "6":
        change_priority(tasks)
        save_tasks(tasks, verbose=False)

    elif choice == "7":
        edit_task(tasks)
        save_tasks(tasks, verbose=False)

    elif choice == "8":
        show_stats(tasks)

    elif choice == "9":
        sorting_task(tasks)
        save_tasks(tasks, verbose=False)

    elif choice == "10":
        search_task(tasks)

    else:
        print("\nНе верный выбор. Попробуйте снова.")

#Таск-Менеджер