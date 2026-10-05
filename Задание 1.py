import random
import statistics
import matplotlib.pyplot as plt

# 1. ФОРМИРОВАНИЕ ВЫБОРКИ

# Количество измерений
n = 100

# Для повторяемости эксперимента.
# При каждом запуске будут генерироваться одинаковые значения.
random.seed(42)

# Формируем выборку времени задержки сети, мс.
# Среднее значение около 20 мс, стандартное отклонение около 3 мс.
measurements = [
    max(0, random.gauss(20, 3))
    for _ in range(n)
]


# 2. РАСЧЁТ СТАТИСТИЧЕСКИХ ХАРАКТЕРИСТИК

sample_size = len(measurements)
minimum = min(measurements)
maximum = max(measurements)
mean = statistics.mean(measurements)
median = statistics.median(measurements)
variance = statistics.variance(measurements)
std_dev = statistics.stdev(measurements)


# 3. ВЫВОД РЕЗУЛЬТАТОВ

print("Статистические характеристики выборки")
print("-" * 50)

print(f"Объём выборки:                 {sample_size}")
print(f"Минимальное значение:          {minimum:.3f} мс")
print(f"Максимальное значение:         {maximum:.3f} мс")
print(f"Среднее арифметическое:        {mean:.3f} мс")
print(f"Медиана:                       {median:.3f} мс")
print(f"Дисперсия:                     {variance:.3f} мс²")
print(f"Среднеквадратическое отклонение: {std_dev:.3f} мс")


# 4. ГРАФИК ПОСЛЕДОВАТЕЛЬНОСТИ ИЗМЕРЕНИЙ

plt.figure(figsize=(10, 5))

plt.plot(
    range(1, sample_size + 1),
    measurements,
    marker="o",
    markersize=3,
    linewidth=1
)

# Дополнительно показываем среднее значение
plt.axhline(
    y=mean,
    linestyle="--",
    label=f"Среднее = {mean:.2f} мс"
)

plt.title("Последовательность измерений сетевой задержки")
plt.xlabel("Номер измерения")
plt.ylabel("Задержка, мс")

plt.grid(True)
plt.legend()
plt.tight_layout()

plt.show()


# 5. ГИСТОГРАММА РАСПРЕДЕЛЕНИЯ

plt.figure(figsize=(10, 5))

plt.hist(
    measurements,
    bins=10,
    edgecolor="black"
)

plt.axvline(
    mean,
    linestyle="--",
    label=f"Среднее = {mean:.2f} мс"
)

plt.axvline(
    median,
    linestyle=":",
    label=f"Медиана = {median:.2f} мс"
)

plt.title("Гистограмма распределения сетевой задержки")
plt.xlabel("Задержка, мс")
plt.ylabel("Количество измерений")

plt.grid(axis="y")
plt.legend()
plt.tight_layout()

plt.show()


# 6. КРАТКИЙ АВТОМАТИЧЕСКИЙ ВЫВОД

print("\nАнализ результатов")
print("-" * 50)

print(
    f"Большинство результатов измерений располагается "
    f"вблизи среднего значения {mean:.2f} мс."
)

print(
    f"Среднеквадратическое отклонение составляет "
    f"{std_dev:.2f} мс."
)

print(
    f"Разница между средним значением и медианой составляет "
    f"{abs(mean - median):.2f} мс."
)

if abs(mean - median) < std_dev * 0.25:
    print(
        "Среднее арифметическое и медиана близки, "
        "что свидетельствует об отсутствии выраженной асимметрии "
        "в полученной выборке."
    )
else:
    print(
        "Наблюдается заметное различие между средним и медианой, "
        "что может свидетельствовать об асимметрии распределения."
    )