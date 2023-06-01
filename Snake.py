from tkinter import *
from PIL import ImageTk, Image
from random import randint
from tkinter import messagebox

# Переменные const:
WIDTH = 840  # Ширина окна
HEIGHT = 840  # Длина окна
BODYSIZE = 40  # Размер одной ячейки
CountBodyW = WIDTH / BODYSIZE  # Кол-во ячеек в окне по ширине
CountBodyH = HEIGHT / BODYSIZE  # Кол-во ячеек в окне по длине
STARTDELAY = 200  # Начальная скорость змейки (для таймера)
LENGTH = 3  # Начальная длина змейки
MINDELAY = 100  # Максимальная скорость змейки (для таймера)
STEPDELAY = 20  # При съедании яблока, скорость будет увеличиваться на STEPDELAY

class Snake(Canvas):
    # Свойства класса:
    headImage, head, body, apple = False, False, False, False
    delay = 0
    direction = 0
    loss = False
    directiontemp = "Right"
    x, y = False, False
    eat_apple = 0
    record = 0
    length_snake = 3
    timer_stop = False

    def __init__(self):
        Canvas.__init__(self, width=WIDTH, height=HEIGHT, bg="Black", highlightthickness=0)
        self.focus_get()  # Фокус на окно
        self.bind_all("<Key>", self.onKeyPressed)  # События для всех нажатий клавишь
        self.MainMenu()
        self.pack()

    # Основное меню
    def MainMenu(self):
        self.create_text(WIDTH / 2, HEIGHT / 4, text="\"Пробел\" - Пауза игры", fill="White", anchor="center", font=("Tahoma", 18))
        start_btn = Button(self, text="Старт", width=15, height=2, cursor="hand2", bg="#C3FF00", fg="Black")
        exit_btn = Button(self, text="Выйти из игры", width=15, height=2, cursor="hand2", bg="#C3FF00", fg="Black")
        self.create_window(WIDTH / 2, HEIGHT / 2.5, window=start_btn, anchor="center", tag="btn")
        self.create_window(WIDTH / 2, HEIGHT / 1.8, window=exit_btn, anchor="center", tag="btn")
        start_btn.bind("<Button-1>", self.StartGame)
        exit_btn.bind("<Button-1>", self.Exit)

    # Начало игры
    def StartGame(self, event):
        self.delete(ALL)
        self.LoadResources()
        self.beginplay()

    # Подготовка изображений
    def LoadResources(self):
        self.headImage = Image.open("images\head.png")
        self.head = ImageTk.PhotoImage(self.headImage.resize((BODYSIZE, BODYSIZE), Image.ANTIALIAS))
        self.body = ImageTk.PhotoImage(Image.open(r"images\body.png").resize((BODYSIZE, BODYSIZE), Image.ANTIALIAS))
        self.apple = ImageTk.PhotoImage(Image.open(r"images\apple.png").resize((BODYSIZE, BODYSIZE), Image.ANTIALIAS))

    # Начало игры
    def beginplay(self):
        self.delay = STARTDELAY  # Начальная скорость змейки (для таймера)
        self.direction = "Right"  # Направление змейки
        self.directiontemp = "Right"  # Временное направление змейки (при нажатии пользователя)
        self.loss = False  # Проигрыш
        self.x = [0] * int(CountBodyW)  # Массив координат x и y
        self.y = [0] * int(CountBodyH)
        self.eat_apple = 0  # Количество съеденых яблок
        self.length_snake = 3  # Длина змейки
        self.timer_stop = False

        file = open(r"files\Record.txt", "r")
        self.record = int(file.read())  # Рекорд длины змейки игрока
        file.close()

        self.delete(ALL)  # Удаляем всё с окна
        self.SpawnActors()
        self.after(self.delay, self.timer)

    # Загружаем голову и тело на окно
    def SpawnActors(self):
        self.x[0] = int(CountBodyW / 2) * BODYSIZE  # Координаты головы x и y
        self.y[0] = int(CountBodyH / 2) * BODYSIZE
        for i in range(LENGTH - 1, 0, -1):  # Координаты тела змейки x и y
            self.x[i] = self.x[0] - BODYSIZE * i
            self.y[i] = self.x[0]
        # Загружаем изображение головы и тела:
            self.create_image(self.x[i], self.y[i], image=self.body, anchor="nw", tag="body")  # загружаем изображения
        self.create_image(self.x[0], self.y[0], image=self.head, anchor="nw", tag="head")

        self.SpawnApple()

    # Загружаем яблоко
    def SpawnApple(self):
        apple = self.find_withtag("apple")  # Находим объект по тегу
        if apple:
            self.delete(apple[0])  # Удаляем с окна если есть яблоко
        # Рандомно расставляем яблоко
        rx = randint(0, int(CountBodyW) - 1) * BODYSIZE
        ry = randint(0, int(CountBodyH) - 1) * BODYSIZE
        self.create_image(rx, ry, image=self.apple, anchor="nw", tag="apple")

    # Таймер игры (выполняется пока не прогиграем)
    def timer(self):
        self.CheckCollisions()  # Проверка столкновения
        if not self.loss:  # Если не проиграл
            if self.timer_stop:  # Если был нажат таймер
                self.Pause()
            else:
                self.CheckApple()  # Проверка съедания яблока
                self.UpdateDirection()  # Изменяет направление головы змейки
                self.MoveSnake()  # Двигаем змейку

                self.CountApple()  # Отображение съеденных яблок
                self.Length_Snake()  # Отображение длины змейки
                self.Records()  # Отображение рекорда игрока

                self.after(self.delay, self.timer)
        else:
            self.GameOver()

    # Обработка при нажатии на клавиатуру
    def onKeyPressed(self, event):
        key = event.keysym
        if not self.timer_stop:
            if key == "Left" and self.direction != "Right":
                self.directiontemp = key
            if key == "Right" and self.direction != "Left":
                self.directiontemp = key
            if key == "Up" and self.direction != "Down":
                self.directiontemp = key
            if key == "Down" and self.direction != "Up":
                self.directiontemp = key
            if key == "space" and not self.loss:
                self.timer_stop = True
        else:
            if key == "Return" and not self.loss:
                self.timer_stop = False
                self.delete("stop")
                self.timer()
        if key == "space" and self.loss:
            self.StartGame("")

    # Двигаем змейку
    def MoveSnake(self):
        head = self.find_withtag("head")
        body = self.find_withtag("body")
        items = body + head
        for i in range(len(items) - 1):
            current_xy = self.coords(items[i])  # Находим координаты тела
            next_xy = self.coords(items[i + 1])  # Следующие координаты тела
            self.move(items[i], next_xy[0] - current_xy[0], next_xy[1] - current_xy[1])  # Двигаем тело
        # Двигаем голову по заданному направлению
        if self.direction == "Left":
            self.move(head, -BODYSIZE, 0)
        if self.direction == "Right":
            self.move(head, BODYSIZE, 0)
        if self.direction == "Up":
            self.move(head, 0, -BODYSIZE)
        if self.direction == "Down":
            self.move(head, 0, BODYSIZE)

    # Проверка съедания яблока с помощью коллизии
    def CheckApple(self):
        apple = self.find_withtag("apple")[0]
        head = self.find_withtag("head")
        body = self.find_withtag("body")[-1]
        x1, y1, x2, y2 = self.bbox(head)  # Возвращает координаты коллизии объекта
        overlaps = self.find_overlapping(x1, y1, x2, y2)
        for actor in overlaps:
            if actor == apple:
                tempx, tempy = self.coords(body)  # Находим координаты последнего объекта тела
                self.SpawnApple()
                self.create_image(tempx, tempy, image=self.body, anchor="nw", tag="body")  # Добавляем +1 тело
                if self.delay > MINDELAY:  # Если скорость змейки на данный момент > максимально поставленной:
                    self.delay -= STEPDELAY  # Уменьшаем скорость на "STEPDELAY" (увеличиваем скорость)
                self.delete("eat")
                self.eat_apple += 1
                self.length_snake += 1

    # Изменяет направление головы змейки
    def UpdateDirection(self):
        self.direction = self.directiontemp
        head = self.find_withtag("head")
        headx, heady = self.coords(head)  # Координаты головы
        self.delete(head)  # Удаляем голову
        if self.direction == "Left":
            # transpose - переворачивает зеркально изображение.
            self.head = ImageTk.PhotoImage(self.headImage.transpose(Image.FLIP_LEFT_RIGHT).resize((BODYSIZE, BODYSIZE), Image.ANTIALIAS))
        else:
            # rotate - переворачивает изображение(в параметре градусы)
            rotates = {"Right": 0, "Up": 90, "Down": -90}
            self.head = ImageTk.PhotoImage(self.headImage.rotate(rotates[self.direction]).resize((BODYSIZE, BODYSIZE), Image.ANTIALIAS))
        self.create_image(headx, heady, image=self.head, anchor="nw", tag="head")  # загружаем голову

    # Проверка столкновения с помощью коллизии
    def CheckCollisions(self):
        body = self.find_withtag("body")
        head = self.find_withtag("head")
        x1, y1, x2, y2 = self.bbox(head)  # Возвращает координаты коллизии объекта
        overlaps = self.find_overlapping(x1, y1, x2, y2)  # Находит объекты которые находится в данной указанной коллизии
        for b in body:
            for actor in overlaps:
                if actor == b:
                    self.loss = True
        # Проверка, не вышла ли голова за пределы окна:
        if x1 < 0:
            self.loss = True
        if x2 > WIDTH:
            self.loss = True
        if y1 < 0:
            self.loss = True
        if y2 > HEIGHT:
            self.loss = True

    # Пауза игры
    def Pause(self):
        self.directiontemp = self.direction
        self.create_text(WIDTH / 2, HEIGHT / 18, text="Пауза", fill="White", anchor="center", font=("Tahoma", 15), tag="stop")
        self.create_text(WIDTH / 2, HEIGHT / 12, text="(Enter - Продолжить)", fill="White", anchor="center", font=("Tahoma", 15), tag="stop")

    # Отображение съеденных яблок
    def CountApple(self):
        self.create_text(WIDTH / 7.8, HEIGHT / 65, text=f"Кол-во съеденных яблок: {self.eat_apple}", fill="White", anchor="center", font=("Tahoma", 12), tag="eat")

    # Отображение длины змейки
    def Length_Snake(self):
        self.create_text(WIDTH / 2, HEIGHT / 65, text=f"Длина змейки: {self.length_snake}", fill="White", anchor="center", font=("Tahoma", 12), tag="eat")

    # Отображение рекорда игрока
    def Records(self):
        if self.length_snake > self.record:
            record = self.length_snake
        else:
            record = self.record
        self.create_text(WIDTH / 1.14, HEIGHT / 65, text=f"Рекорд длины змейки: {record}", fill="White", anchor="center", font=("Tahoma", 12), tag="eat")

    # Конец игры
    def GameOver(self):
        self.delete(ALL)
        self.create_text(self.winfo_width() / 2, self.winfo_height() / 2 - 200, text="Вы проиграли", fill="White", font=("Tahoma", 22), tag="text")
        if self.length_snake > self.record:
            self.create_text(self.winfo_width() / 2, self.winfo_height() / 2 - 100, text=f"У вас новый рекорд по длине змейки: {self.length_snake}", fill="White", font=("Tahoma", 22), tag="text")
            file = open(r"files\Record.txt", "w")
            file.write(str(self.length_snake))
            file.close()
        else:
            self.create_text(self.winfo_width() / 2, self.winfo_height() / 2 - 100, text=f"Длина змейки: {self.length_snake}", fill="White", font=("Tahoma", 22), tag="text")
        self.create_text(self.winfo_width() / 2, self.winfo_height() / 2, text="Пробел для игры заново", fill="White", font=("Tahoma", 22), tag="text")

    # Выход из игры
    def Exit(self, event):
        if messagebox.askyesno("Выход из программы", "Хотите выйти?"):
            root.quit()


root = Tk()
root.resizable(False, False)
root.title("Змейка")
root.board = Snake()

ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()

x = int(ws / 2 - WIDTH / 2)
y = int(hs / 2 - HEIGHT / 2)
root.geometry("+{0}+{1}".format(x, y))

root.mainloop()
