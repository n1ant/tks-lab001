import random
import statistics
import math
import matplotlib.pyplot as plt
from scipy.stats import t


# ============================================================
# 1. ИСХОДНАЯ ВЫБОРКА
# Та же самая, что использовалась в первом задании
# ============================================================

random.seed(42)

measurements = [
    max(0, random.gauss(20, 3))
    for _ in range(100)
]


# ============================================================
# 2. ФУНКЦИЯ РАСЧЁТА СТАТИСТИКИ И ДОВЕРИТЕЛЬНОГО ИНТЕРВАЛА
# ============================================================

def calculate_statistics(sample, confidence=0.95):

    n = len(sample)

    mean = statistics.mean(sample)
    median = statistics.median(sample)
    variance = statistics.variance(sample)
    std_dev = statistics.stdev(sample)

    # Уровень значимости
    alpha = 1 - confidence

    # Критическое значение распределения Стьюдента
    t_critical = t.ppf(1 - alpha / 2, df=n - 1)

    # Стандартная ошибка среднего
    standard_error = std_dev / math.sqrt(n)

    # Погрешность доверительного интервала
    margin_error = t_critical * standard_error

    # Границы доверительного интервала
    confidence_lower = mean - margin_error
    confidence_upper = mean + margin_error

    # Полная ширина доверительного интервала
    interval_width = confidence_upper - confidence_lower

    return {
        "n": n,
        "mean": mean,
        "median": median,
        "variance": variance,
        "std_dev": std_dev,
        "lower": confidence_lower,
        "upper": confidence_upper,
        "width": interval_width
    }


# ============================================================
# 3. ВЫБОРКИ РАЗНОГО РАЗМЕРА
# ============================================================

sample_sizes = [10, 20, 30, 50, 100]

results = []

for size in sample_sizes:

    # Берём первые size измерений исходной выборки
    sample = measurements[:size]

    result = calculate_statistics(sample)

    results.append(result)


# ============================================================
# 4. ВЫВОД ТАБЛИЦЫ
# ============================================================

print("Статистические характеристики выборок")
print("-" * 105)

print(
    f"{'N':>5} "
    f"{'Среднее':>12} "
    f"{'Медиана':>12} "
    f"{'Дисперсия':>12} "
    f"{'СКО':>10} "
    f"{'Нижняя гр.':>13} "
    f"{'Верхняя гр.':>13} "
    f"{'Ширина ДИ':>12}"
)

print("-" * 105)

for r in results:
    print(
        f"{r['n']:>5} "
        f"{r['mean']:>12.3f} "
        f"{r['median']:>12.3f} "
        f"{r['variance']:>12.3f} "
        f"{r['std_dev']:>10.3f} "
        f"{r['lower']:>13.3f} "
        f"{r['upper']:>13.3f} "
        f"{r['width']:>12.3f}"
    )


# ============================================================
# 5. ГРАФИК ШИРИНЫ ДОВЕРИТЕЛЬНОГО ИНТЕРВАЛА
# ============================================================

sizes = [r["n"] for r in results]
widths = [r["width"] for r in results]

plt.figure(figsize=(9, 5))

plt.plot(
    sizes,
    widths,
    marker="o"
)

plt.title(
    "Зависимость ширины доверительного интервала\n"
    "от количества измерений"
)

plt.xlabel("Количество измерений")
plt.ylabel("Ширина 95%-го доверительного интервала, мс")

plt.grid(True)
plt.tight_layout()
plt.show()


# ============================================================
# 6. ДОПОЛНИТЕЛЬНЫЙ ГРАФИК СРЕДНЕГО
# ============================================================

means = [r["mean"] for r in results]

plt.figure(figsize=(9, 5))

plt.plot(
    sizes,
    means,
    marker="o"
)

plt.axhline(
    statistics.mean(measurements),
    linestyle="--",
    label="Среднее полной выборки"
)

plt.title("Изменение среднего значения при увеличении выборки")
plt.xlabel("Количество измерений")
plt.ylabel("Средняя задержка, мс")

plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()