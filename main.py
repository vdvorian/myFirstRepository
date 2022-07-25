import sys

import PyQt5   # библиотека GUI (графического интерфейса пользователя)
from PyQt5.QtGui import QFont, QPixmap, QRegExpValidator
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QDesktopWidget
from PyQt5.QtCore import pyqtSlot, QRegExp, Qt
from PyQt5.QtGui import QPainter, QPen, QBrush

import matplotlib   # библиотека для рисования графиков
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from science import HS_k, HS_n, SCA   # импортирую методы для построения графиков


class PlotCanvas(FigureCanvas):   # класс графика

    def __init__(self, title, xlabel, ylabel, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)   # создаю поле для рисования графика
                                                              # (размер 5*4 дюймов, 100 пикселей на дюйм)
        self.fig.set_facecolor('#f0f0f0')
        FigureCanvas.__init__(self, self.fig)   # вызываю конструктор класса-родителя
        self.setParent(parent)   # указываю, что PlotCanvas должен быть отрисован в главном QWidget-е
        self.parent = parent
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel

        matplotlib.pyplot.rcParams['font.size'] = 14
        matplotlib.pyplot.rcParams['font.family'] = 'Lucida Console'
        self.fig.subplots_adjust(bottom=0.15, left=0.20)

        FigureCanvas.updateGeometry(self)
        self.ax = self.figure.add_subplot(111)   # создаю оси, на которых будет рисоваться график

        # задаю начальный вид графиков
        self.set_labels()
        self.ax.grid()
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(10, 50)
        plt.tight_layout()

    def set_labels(self, title_size=20, label_size=10):   # устанавливает стиль и размер шрифта лейблов графика
        hfont = {"size": title_size}
        hfont_labels = {"size": label_size}
        self.ax.set_title(self.title, **hfont)
        self.ax.set_xlabel(self.xlabel, **hfont_labels)
        self.ax.set_ylabel(self.ylabel, **hfont_labels)

    def plot(self, k, n, func):   # строит графики K* и G* (пока только границы HS)
        x = []
        yk_lower = []
        yk_higher = []

        # заполняю массивы абсцисс и ординат
        for i in range(201):
            x.append(i / 2)
        for i in range(201):
            HS_bounds = func(k, n, x[i])
            yk_lower.append(HS_bounds[0])
            yk_higher.append(HS_bounds[1])

        # дествия при каждой перерисовке графика
        self.ax.cla()   # очищаю график
        self.set_labels()   # выставляю лейблы
        self.ax.plot(x, yk_lower, 'b-')   # рисую нижнюю границу HS
        self.ax.plot(x, yk_higher, 'r-')   # рисую верхнюю границу HS
        self.ax.grid()   # разлиновываю полотно графика
        self.draw()   # рисую график со всеми изменениями


class PlotBulkBounds(PlotCanvas):   # класс графика для K* (наследую от PlotCanvas)

    def __init__(self, title, xlabel, ylabel, parent=None, width=5, height=4, dpi=100):
        super().__init__(title, xlabel, ylabel, parent, width, height, dpi)

    def mouseDoubleClickEvent(self, event):   # переопределяю метод двойного клика
        self.parent.changeGraphSize('k')

    def plot(self, k, n, a):   # перерисовывает график K*
        super().plot(k, n, HS_k)
        if a[0] != 0 and a[1] != -1:   # рисую черную линию (SCA) и ставлю черную жирную точку
            sca = SCA(k, n, a)
            self.ax.plot([p * 100 for p in sca[2]], sca[0], 'k-')
            self.draw()


class PlotShearBounds(PlotCanvas):   # класс графика для G* (наследую от PlotCanvas)

    def __init__(self, title, xlabel, ylabel, parent=None, width=5, height=4, dpi=100):
        super().__init__(title, xlabel, ylabel, parent, width, height, dpi)

    def mouseDoubleClickEvent(self, event):   # переопределяю метод двойного клика
        self.parent.changeGraphSize('n')

    def plot(self, k, n, a):   # перерисовывает график G*
        super().plot(k, n, HS_n)
        if a[0] != 0 and a[1] != -1:   # рисую черную линию (SCA) и ставлю черную жирную точку
            sca = SCA(k, n, a)
            self.ax.plot([p * 100 for p in sca[2]], sca[1], 'k-')
            self.draw()


class Demo(QWidget):
    # объявляю все переменные

    # параметры окна программы
    window_width = 1040
    window_height = 900
    space_above_all = 50
    shift_from_vertical_axis = 350
    picture_side = 200

    # для работы с "ползунком"
    initial_proportion = 60
    proportion_input = 0
    proportion_to_draw = 0
    pics = []
    composite_pictures = []

    # переменные для создания и работы с виджетами
    names = ['K1', 'G1', 'K2', 'G2']
    asp_names = ['a1', 'a2']
    inputs = {}
    asp_inputs = {}
    ef_inputs = []
    ef_labels = []
    k_graph = None
    n_graph = None

    n = [0, 0]
    k = [0, 0]
    a = [0, 0]

    # флаги (переменные состояния)
    graph_zoomed = False
    changed_by_mouse = False
    mouse_left_down = False


    def __init__(self):   # конструктор класса
        super().__init__()   # вызываю конструктор суперкласса (QWidget)
        self.initUI()        # вызываю мой нижеописанный метод (где буду создавать все виджеты в окне)
        self.setMouseTracking(True)   # чтобы следить за событиями mouse move и прочими событиями, связянными с мышью

    def changeGraphSize(self, name):   # изменяет размер графиков при двойном нажатии мыши по ним
        if self.graph_zoomed:
            if name == 'n':
                self.n_graph.fig.subplots_adjust(bottom=0.15, left=0.20)
                self.n_graph.setGeometry(505, 430, 500, 400)
                self.n_graph.set_labels()
                self.n_graph.draw()
            else:  # name == 'k'
                self.k_graph.fig.subplots_adjust(bottom=0.15, left=0.20)
                self.k_graph.setGeometry(25, 430, 500, 400)
                self.k_graph.set_labels()
                self.k_graph.draw()
        else:
            if name == 'n':
                self.n_graph.fig.subplots_adjust(bottom=0.1, left=0.15)
                self.n_graph.setGeometry(0, -20, self.window_width, self.window_height)
                self.n_graph.set_labels(title_size=25, label_size=15)
                self.n_graph.draw()
                self.n_graph.raise_()
            else:  # name == 'k'
                self.k_graph.fig.subplots_adjust(bottom=0.1, left=0.15)
                self.k_graph.setGeometry(0, -20, self.window_width, self.window_height)
                self.k_graph.set_labels(title_size=25, label_size=15)
                self.k_graph.draw()
                self.k_graph.raise_()

        self.graph_zoomed = not self.graph_zoomed

    def initUI(self):   # создает все виджеты в главном окне
        self.setWindowTitle('composite maker')

        labels = {}
        asp_labels = {}

        for i in range(2):   # квадратики компонент (синий и голубой)
            self.pics.append(QLabel(self))
            pixmap = QPixmap(f'rectangle{i + 1}.png')
            self.pics[i].setPixmap(pixmap)
            self.pics[i].move(
                self.window_width // 2 - ((-1) ** i) * self.shift_from_vertical_axis - i * self.picture_side,
                self.space_above_all)

        for i in range(len(self.names)):   # инпуты K1, G1, K2, G2
            labelName = self.names[i]
            labels[labelName] = QLabel(labelName, self)
            labels[labelName].move(self.window_width // 2 - ((-1) ** (i // 2)) * self.shift_from_vertical_axis - (
                    i // 2) * self.picture_side,
                                   self.space_above_all + self.picture_side + 20 + (i % 2) * 50)
            labels[labelName].setFont(QFont('Lucida Console', 14))

            self.inputs[labelName] = QLineEdit(self)
            self.inputs[labelName].setPlaceholderText("20")
            # устанавливаю валидатор на инпуты с помощью регулярных выражений
            reg_ex = QRegExp("(^200$)|(((^1[0-9]{0,2})|(^[1-9][0-9]?))(\.\d{1,2}$)?)")
            input_validator = QRegExpValidator(reg_ex, self.inputs[labelName])
            self.inputs[labelName].setValidator(input_validator)
            self.inputs[labelName].setGeometry(
                self.window_width // 2 - ((-1) ** (i // 2)) * self.shift_from_vertical_axis - (
                        i // 2) * self.picture_side + 45,
                self.space_above_all + self.picture_side + 20 + (i % 2) * 50 - 5, 155, 40)
            self.inputs[labelName].setFont(QFont('Lucida Console', 13))
            # устанавливаю метод на событие изменения текса в инпутах
            self.inputs[labelName].textChanged.connect(self.inputsChangeEvent)

        for i in range(len(self.asp_names)):   # инпуты a1, a2
            labelName = self.asp_names[i]
            asp_labels[labelName] = QLabel(labelName, self)
            asp_labels[labelName].move(self.window_width // 2 - ((-1) ** (i % 2)) * self.shift_from_vertical_axis - (
                    i % 2) * self.picture_side,
                                       self.space_above_all + self.picture_side + 120)
            asp_labels[labelName].setFont(QFont('Lucida Console', 14))

            self.asp_inputs[labelName] = QLineEdit(self)
            self.asp_inputs[labelName].setPlaceholderText("20")
            reg_ex = QRegExp("(^1$)|((^0)((\.[1-9][0-9]?$)|(\.0[1-9]$)))")
            asp_input_validator = QRegExpValidator(reg_ex, self.asp_inputs[labelName])
            self.asp_inputs[labelName].setValidator(asp_input_validator)
            self.asp_inputs[labelName].setGeometry(
                self.window_width // 2 - ((-1) ** (i % 2)) * self.shift_from_vertical_axis - (
                        i % 2) * self.picture_side + 45,
                self.space_above_all + self.picture_side + 115, 155, 40)
            self.asp_inputs[labelName].setFont(QFont('Lucida Console', 13))
            self.asp_inputs[labelName].textChanged.connect(self.inputsChangeEvent)

        self.composite()   # вызываю метод "ползунка"

        self.setFixedWidth(self.window_width)   # фиксирую размеры окна (чтобы нельзя было изменять)
        self.setFixedHeight(self.window_height)

        # отрисовываю графики
        self.k_graph = PlotBulkBounds(title='K*', parent=self, xlabel='volume fraction of material 1',
                                        ylabel='effective bulk modulus (GPa)')
        self.k_graph.setGeometry(25, 430, 500, 400)

        self.n_graph = PlotShearBounds(title='G*', xlabel='volume fraction of material 1',
                                         ylabel='effective shear modulus (GPa)', parent=self)
        self.n_graph.setGeometry(505, 430, 500, 400)

        labelName = ["K*", "G*"]
        for i in range(2):   # нередактируемые инпуты, где будут выводиться значения K* и G*
            self.ef_labels.append(QLabel(labelName[i], self))
            self.ef_labels[i].move(self.window_width // 2 - 100,
                                   self.space_above_all + self.picture_side + 20 + (i % 2) * 50)
            self.ef_labels[i].setFont(QFont('Lucida Console', 14))

            self.ef_inputs.append(QLineEdit(self))
            self.ef_inputs[i].setReadOnly(True)
            self.ef_inputs[i].setGeometry(self.window_width // 2 - 55,
                                          self.space_above_all + self.picture_side + 20 + (i % 2) * 50 - 5, 155, 40)
            self.ef_inputs[i].setFont(QFont('Lucida Console', 13))

        self.center()   # вызываю метод, который будет при запуске программы ставить окно по центру
        self.show()

    def inputsChangeEvent(self):   # метод, который вызывается при любом изменении инпутов K1, G1, a1, K2, G2, a2
        try:    # пытаюсь считать значения инпутов а1, а2 в массив а
            self.a = [float(self.asp_inputs['a1'].text()), float(self.asp_inputs['a2'].text())]
        except:   # если не получается, присваиваю а = [-1, -1]
            self.a = [-1, -1]

        try:   # пытаюсь считать ВСЕ 4 значения K1, G1, K2, G2
            self.n = [float(self.inputs['G1'].text()), float(self.inputs['G2'].text())]
            self.k = [float(self.inputs['K1'].text()), float(self.inputs['K2'].text())]

            # если получилось, строю графики (вызываю метод plot из классов PlotBulkBounds и PlotShearBounds)
            self.k_graph.plot(self.k, self.n, self.a)
            self.n_graph.plot(self.k, self.n, self.a)
        except:   # если не получилось, ничего не делаю
            pass

        else:   # else после try-except выполняется только тогда, когда не было ни одной ошибки
            # если считались a1 и а2, отрисовываю черную линию SCA
            if self.a[0] > 0 and self.a[1] > 0 and self.proportion_input.text() != '':
                sca = SCA(self.k, self.n, self.a)
                if float(self.proportion_input.text()) != 0 and float(self.proportion_input.text()) != 100:
                    i = sca[2].index(float(self.proportion_input.text()) / 100)
                elif float(self.proportion_input.text()) == 0:
                    i = sca[2].index(float(self.proportion_input.text()) / 100 + 1e-7)
                else:
                    i = sca[2].index(float(self.proportion_input.text()) / 100 - 1e-7)

                # рисую жирные точки
                self.k_graph.ax.scatter(sca[2][i] * 100, sca[0][i], c='black', s=40)
                self.k_graph.draw()
                self.ef_inputs[0].setText(f'{round(sca[0][i], 1):g}')
                self.n_graph.ax.scatter(sca[2][i] * 100, sca[1][i], c='black', s=40)
                self.n_graph.draw()
                self.ef_inputs[1].setText(f'{round(sca[1][i], 1):g}')

    def composite(self):   # отрисовывает центральный "ползунок" и инпут процентов
        for i in range(2):
            self.composite_pictures.append(QLabel(self))
            c_pixmap = QPixmap(f'rectangle{i + 1}.png')
            self.composite_pictures[i].setPixmap(c_pixmap)

        self.composite_pictures[0].move((self.window_width - self.picture_side) // 2, self.space_above_all)
        self.composite_pictures[1].setGeometry((self.window_width - self.picture_side) // 2,
                                               self.space_above_all + self.initial_proportion,
                                               self.picture_side, self.picture_side - self.initial_proportion)

        self.proportion_input = QLineEdit(self)
        self.proportion_input.setGeometry(self.window_width // 2 - 55, self.space_above_all + self.picture_side + 115,
                                          110, 40)
        self.proportion_input.setFont(QFont('Lucida Console', 15))
        self.proportion_input.setText(f'{int(self.initial_proportion) // 2}')
        reg_ex = QRegExp("(^100(\.0{1,2})?$)|(^([1-9]([0-9])?|0))")
        input_validator = QRegExpValidator(reg_ex, self.proportion_input)
        self.proportion_input.setValidator(input_validator)
        self.proportion_input.textChanged.connect(self.proportionInputEvent)

    def proportionInputEvent(self):   # метод, который вызывается при изменении инпута процентов
        if self.proportion_input.text() == "":   # считываю значения инпута
            proportion = 0
        else:
            proportion = float(self.proportion_input.text())

        # двигаю ползунок
        self.composite_pictures[1].setGeometry((self.window_width - self.picture_side) // 2,
                                               self.space_above_all + 2 * round(proportion),
                                               self.picture_side, self.picture_side - 2 * round(proportion))

        # сделано для того, чтобы графики перерисовывались не тогда, когда я двигаю мышь, а тогда,
        # когда я отпускаю ее (иначе сильно тормозит)
        if self.changed_by_mouse:
            self.changed_by_mouse = False
        else:
            self.inputsChangeEvent()

    def mousePressEvent(self, event):   # переопределяю метод нажатия мыши
        if event.button() == PyQt5.QtCore.Qt.LeftButton:   # если нажата левая кнопка мыши
            # если нажатие попало в область "ползунка"
            if ((self.window_width - self.picture_side) // 2 <= event.x() <= (
                    self.window_width + self.picture_side) // 2) and (
                    self.space_above_all <= event.y() <= (self.space_above_all + self.picture_side)):
                self.mouse_left_down = True
                self.mouseMoveEvent(event)   # вызываю метод, который будет следить за движением мыши

    def mouseMoveEvent(self, event):   # переопределяю метод движения мыши
        if self.mouse_left_down:   # если зажата левая кнопка мыши
            if self.space_above_all > event.y():   # смотрю, куда двинули мышку, считываю координату,
                                                   # интрепретирую ее в проценты
                self.proportion_to_draw = self.picture_side
            elif (self.space_above_all + self.picture_side) > event.y():
                self.proportion_to_draw = self.picture_side + self.space_above_all - event.y()
            else:
                self.proportion_to_draw = 0

            self.changed_by_mouse = True
            # меняю значение в инпуте процентов
            self.proportion_input.setText(f'{100 - (100 * self.proportion_to_draw) // self.picture_side}')

    def mouseReleaseEvent(self, event):   # переопределяю метод расжатия кнопок мыши
        if event.button() == PyQt5.QtCore.Qt.LeftButton:
            self.mouse_left_down = False
            self.changed_by_mouse = False
            self.inputsChangeEvent()   # отправляю программу в метод отрисовки графиков при изменении
                                       # инпутов, чтобы перерисовалась жирная точка

    def center(self):   # выставляю окно программы по центру экрана
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


app = QApplication(sys.argv)
demo = Demo()
app.exec_()
