import numpy as np
import matplotlib.pyplot as plt

# --- Параметры ---
R_KM = 6371.0  # Радиус Земли, км
H_KM = 500.0  # Высота орбиты, км


# --- Вычисления ---

# Максимальный угол σ (в радианах), когда вся Земля видна в поле зрения
s_rad_max = np.arcsin(R_KM / (R_KM + H_KM))
# Максимальный угол σ (в градусах)
s_deg_max = np.rad2deg(s_rad_max)

print(f"Радиус Земли (Rз): {R_KM} км")
print(f"Высота орбиты (H): {H_KM} км")
print(f"Максимальный угол 2σ для обзора поверхности: {2 * s_deg_max:.2f} градусов")


def l_of_sigma(s_deg: float) -> float:
    """
    Рассчитывает длину полосы обзора L (км) по углу σ (градусы).
    :param s_deg: Угол σ в градусах
    :return: Длина дуги L (км)
    """
    s_rad = np.deg2rad(s_deg)  # Перевод угла σ из градусов в радианы
    s_rad = min(s_rad, s_rad_max)  # Верхняя граница для угла σ (в радианах)
    return 2 * R_KM * (np.arcsin((R_KM + H_KM) / R_KM * np.sin(s_rad)) - s_rad)  # Формула расчёта длинны дуги L (км)


#  Таблица значений углов 2σ и длин дуг L, при σ = 0, 1, 2, 3...90 град

print('| 2σ, ° | L, км |')
for sigma in range(91):
    l = round(l_of_sigma(sigma), 2)
    print(f'|{" " * (7 - len(str(2 * sigma)))}{2 * sigma}|{" " * (7 - len(str(l)))}{l}|')

# --- Подготовка данных для графика ---

#  Создание массива углов σ в градусах от 0 до 90
sigma_values_deg = [x / 100 for x in range(0, 9000)]
sigma_values_deg.append(s_deg_max)  # Добавление максимального угла σ

# Вычисление соответствующие значения L, используя функцию
L_values_km = [l_of_sigma(s_deg) for s_deg in sigma_values_deg]

#  Создание массива углов 2σ из массива углов σ
two_sigma_values_deg = tuple(map(lambda x: x * 2, sigma_values_deg))

# --- Построение графика ---

plt.figure(figsize=(10, 6))  # Задаем размер рисунка
plt.plot(two_sigma_values_deg, L_values_km, label='L (км)')

# Добавление точки (σ_max, L_max) и пунктиров на график
plt.scatter(
    [2 * s_deg_max],
    [L_values_km[-1]],
    color='red',
    zorder=3,
    label=f'Макс. 2σ = {2 * s_deg_max:.2f}°, L = {L_values_km[-1]:.2f} км')
plt.axvline(
    x=2 * s_deg_max,
    ymin=0,
    ymax=L_values_km[-1] / plt.ylim()[-1],
    color='grey',
    linestyle='--',
    linewidth=0.8,
            )
plt.axhline(
    y=L_values_km[-1],
    xmin=0,
    xmax=2 * s_deg_max / plt.xlim()[-1],
    color='grey',
    linestyle='--',
    linewidth=0.8,
            )

# Настройка внешнего вида графика
plt.xlabel("Угол 2σ (градусы)")  # Подпись оси X
plt.ylabel("Полоса обзора L (км)")  # Подпись оси Y
plt.title("Зависимость полосы обзора (L) от угла сканирования (2σ)")  # Заголовок
plt.grid(True)  # Включение сетки
plt.legend()  # Показ легенды
plt.xlim(left=0)  # Начало оси X с 0
plt.ylim(bottom=0)  # Начало оси Y с 0
plt.xticks([x for x in range(0, 181, 10)])  # Метки на оси X
plt.yticks([y for y in range(0, 5001, 500)])  # Метки на оси Y

# Показать график
plt.show()
