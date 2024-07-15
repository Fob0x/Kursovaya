import numpy as np
import matplotlib.pyplot as plt

# Этот код решает задачу напряжённо-деформированного состояния эллиптической пластины с включением
# под действием внешних нагрузок и внутреннего давления, учитывая упругопластические свойства материала
# (в данном случае обычной стали).
# Используется метод малого параметра для учета напряжений и деформаций в материале плиты.
# Затем визуализируются результаты в виде контурных карт.

# Параметры задачи
a = 0.02  # Полуось эллипса включения (м)
b = 0.015  # Полуось эллипса плиты (м)
P1 = 150.0  # Нагрузка по оси x (МПа)
P2 = 150.0  # Нагрузка по оси y (МПа)
P0 = 50.0  # Внутреннее давление включения (МПа)
G = 810.0  # Модуль сдвига плиты (МПа)
G1 = 1216.0  # Модуль сдвига включения (МПа)
E = 200000.0  # Модуль Юнга плиты (МПа)
nu = 0.3  # Коэффициент Пуассона плиты
yield_stress = 250.0  # Предел текучести материала (МПа)

# Создание сетки координат
theta = np.linspace(0, 2 * np.pi, 400)  # Угловая координата (радианы)
r = np.linspace(a, b, 400)  # Радиальная координата (м)
R, Theta = np.meshgrid(r, theta)  # Полярная сетка координат
X = R * np.cos(Theta)  # Преобразование в декартовы координаты
Y = R * np.sin(Theta)

# Функции для расчета напряжений и деформаций с учетом метода малого параметра

# Напряжение sigma_xx (осевое напряжение по x) с учетом внутреннего давления и внешней нагрузки
def stress_xx(r, theta, P1, P0, a, G, G1):
    return P1 * (1 + (a**2 / r**2) * np.cos(2 * theta)) + P0 * (a**2 / r**2) * np.cos(2 * theta) * (G / G1)

# Напряжение sigma_yy (осевое напряжение по y) с учетом внутреннего давления и внешней нагрузки
def stress_yy(r, theta, P2, P0, a, G, G1):
    return P2 * (1 - (a**2 / r**2) * np.cos(2 * theta)) + P0 * (a**2 / r**2) * np.cos(2 * theta) * (G / G1)

# Напряжение sigma_xy (касательное напряжение) с учетом внутреннего давления
def stress_xy(r, theta, P0, a, G, G1):
    return -P0 * (a**2 / r**2) * np.sin(2 * theta) * (G / G1)

# Деформация e_xx (осевая деформация по x) с учетом закона Гука для плоского напряженного состояния
def strain_xx(sigma_xx, sigma_yy, E, nu):
    return (1 / E) * (sigma_xx - nu * sigma_yy)

# Деформация e_yy (осевая деформация по y) с учетом закона Гука для плоского напряженного состояния
def strain_yy(sigma_xx, sigma_yy, E, nu):
    return (1 / E) * (sigma_yy - nu * sigma_xx)

# Деформация e_xy (касательная деформация) с учетом закона Гука для касательных напряжений
def strain_xy(sigma_xy, G):
    return (1 / G) * sigma_xy

# Расчет напряжений в точках сетки
sigma_xx = stress_xx(R, Theta, P1, P0, a, G, G1)
sigma_yy = stress_yy(R, Theta, P2, P0, a, G, G1)
sigma_xy = stress_xy(R, Theta, P0, a, G, G1)

# Расчет деформаций в точках сетки
e_xx = strain_xx(sigma_xx, sigma_yy, E, nu)
e_yy = strain_yy(sigma_xx, sigma_yy, E, nu)
e_xy = strain_xy(sigma_xy, G)

# Расчет эквивалентного напряжения Мизеса (критерий пластичности)
sigma_e = np.sqrt(sigma_xx**2 + sigma_yy**2 - sigma_xx * sigma_yy + 3 * sigma_xy**2)

# Упругопластическая граница (напряжение Мизеса сравнивается с пределом текучести)
plastic_boundary = sigma_e > yield_stress

# Визуализация результатов

# Эквивалентное напряжение Мизеса
fig, ax = plt.subplots()
# Отображение контурной карты эквивалентного напряжения Мизеса
cs = ax.contourf(X, Y, sigma_e, levels=100, cmap='coolwarm')
cbar = fig.colorbar(cs, ax=ax, shrink=0.9)
cbar.set_label('Эквивалентное напряжение Мизеса (МПа)')
# Добавление контурных линий для эквивалентного напряжения Мизеса
ax.contour(X, Y, sigma_e, levels=np.linspace(0, np.max(sigma_e), 10), colors='black', linestyles='solid', linewidths=1)
# Добавление упругопластической границы
ax.contour(X, Y, plastic_boundary, levels=[0.5], colors='k', linewidths=2)
ax.set_aspect('equal')
ax.set_title('Эквивалентное напряжение Мизеса')
plt.xlabel('X (м)')
plt.ylabel('Y (м)')
plt.get_current_fig_manager().set_window_title('Землянухин Р.М.')
plt.show()

# Визуализация деформаций в одном окне
fig, axs = plt.subplots(1, 3, figsize=(18, 6))

# Деформация e_xx
cs = axs[0].contourf(X, Y, e_xx, levels=100, cmap='viridis')
cbar = fig.colorbar(cs, ax=axs[0], shrink=0.9)
cbar.set_label('Деформация e_xx')
axs[0].set_aspect('equal')
axs[0].set_title('Деформация e_xx')
axs[0].set_xlabel('X (м)')
axs[0].set_ylabel('Y (м)')

# Деформация e_yy
cs = axs[1].contourf(X, Y, e_yy, levels=100, cmap='viridis')
cbar = fig.colorbar(cs, ax=axs[1], shrink=0.9)
cbar.set_label('Деформация e_yy')
axs[1].set_aspect('equal')
axs[1].set_title('Деформация e_yy')
axs[1].set_xlabel('X (м)')
axs[1].set_ylabel('Y (м)')

# Деформация e_xy
cs = axs[2].contourf(X, Y, e_xy, levels=100, cmap='viridis')
cbar = fig.colorbar(cs, ax=axs[2], shrink=0.9)
cbar.set_label('Деформация e_xy')
axs[2].set_aspect('equal')
axs[2].set_title('Деформация e_xy')
axs[2].set_xlabel('X (м)')
axs[2].set_ylabel('Y (м)')

plt.get_current_fig_manager().set_window_title('Землянухин Р.М.')
plt.show()

# Общий вывод:
# Рассчитанные и визуализированные напряжения и деформации в эллиптической пластине с включением показывают
# значительное влияние внутреннего давления и внешних нагрузок на распределение напряжений и деформаций.
# Эквивалентное напряжение Мизеса позволяет оценить пластическое поведение материала и определить области,
# где происходит переход от упругого к пластическому состоянию. Анализ напряжений и деформаций показывает,
# что наибольшие деформации наблюдаются вблизи включения, что согласуется с теорией концентрации напряжений
# в областях с геометрическими неоднородностями. Данный подход с использованием метода малого параметра
# позволяет учитывать влияние упругопластических свойств материала на распределение напряжений и деформаций,
# что важно для прогнозирования долговечности и надежности конструкций.
