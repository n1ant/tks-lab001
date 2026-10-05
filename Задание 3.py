import random
import statistics
import matplotlib.pyplot as plt


# ============================================================
# 1. ФОРМИРОВАНИЕ ИСХОДНОЙ ВЫБОРКИ
# ============================================================

random.seed(42)

measurements = [
    max(0, random.gauss(20, 3))
    for _ in range(100)
]


# ============================================================
# 2. ДОБАВЛЕНИЕ ИСКУССТВЕННЫХ ВЫБРОСОВ
# ============================================================

measurements_with_outliers = measurements.copy()

measurements_with_outliers.extend([
    60,
    80,
    100
])


# ============================================================
# 3. ФУНКЦИЯ РАСЧЁТА СТАТИСТИКИ
# ============================================================

def calculate_statistics(sample):

    return {
        "n": len(sample),
        "min": min(sample),
        "max": max(sample),
        "mean": statistics.mean(sample),
        "median": statistics.median(sample),
        "variance": statistics.variance(sample),
        "std_dev": statistics.stdev(sample)
    }


# ============================================================
# 4. ОБНАРУЖЕНИЕ ВЫБРОСОВ МЕТОДОМ IQR
# ============================================================

def detect_outliers(sample):

    sorted_sample = sorted(sample)

    q1 = statistics.quantiles(
        sorted_sample,
        n=4,
        method="inclusive"
    )[0]

    q3 = statistics.quantiles(
        sorted_sample,
        n=4,
        method="inclusive"
    )[2]

    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = [
        value
        for value in sample
        if value < lower_bound or value > upper_bound
    ]

    return outliers, q1, q3, iqr, lower_bound, upper_bound


# ============================================================
# 5. ПОИСК ВЫБРОСОВ
# ============================================================

outliers, q1, q3, iqr, lower_bound, upper_bound = \
    detect_outliers(measurements_with_outliers)


# ============================================================
# 6. ФОРМИРОВАНИЕ ВЫБОРКИ БЕЗ ВЫБРОСОВ
# ============================================================

clean_measurements = [
    value
    for value in measurements_with_outliers
    if value not in outliers
]


# ============================================================
# 7. РАСЧЁТ СТАТИСТИКИ
# ============================================================

original_stats = calculate_statistics(measurements)

with_outliers_stats = calculate_statistics(
    measurements_with_outliers
)

clean_stats = calculate_statistics(
    clean_measurements
)


# ============================================================
# 8. ВЫВОД РЕЗУЛЬТАТОВ
# ============================================================

print("КРИТЕРИЙ ОБНАРУЖЕНИЯ ВЫБРОСОВ")
print("-" * 60)

print(f"Q1:                         {q1:.3f} мс")
print(f"Q3:                         {q3:.3f} мс")
print(f"IQR:                        {iqr:.3f} мс")
print(f"Нижняя граница:             {lower_bound:.3f} мс")
print(f"Верхняя граница:            {upper_bound:.3f} мс")

print("\nОбнаруженные выбросы:")
print(outliers)


# ============================================================
# 9. СРАВНЕНИЕ СТАТИСТИКИ
# ============================================================

print("\nСРАВНЕНИЕ РЕЗУЛЬТАТОВ")
print("-" * 90)

print(
    f"{'Показатель':<25}"
    f"{'Исходная':>15}"
    f"{'С выбросами':>18}"
    f"{'После удаления':>20}"
)

print("-" * 90)

print(
    f"{'Объём выборки':<25}"
    f"{original_stats['n']:>15}"
    f"{with_outliers_stats['n']:>18}"
    f"{clean_stats['n']:>20}"
)

print(
    f"{'Среднее, мс':<25}"
    f"{original_stats['mean']:>15.3f}"
    f"{with_outliers_stats['mean']:>18.3f}"
    f"{clean_stats['mean']:>20.3f}"
)

print(
    f"{'Медиана, мс':<25}"
    f"{original_stats['median']:>15.3f}"
    f"{with_outliers_stats['median']:>18.3f}"
    f"{clean_stats['median']:>20.3f}"
)

print(
    f"{'Дисперсия, мс²':<25}"
    f"{original_stats['variance']:>15.3f}"
    f"{with_outliers_stats['variance']:>18.3f}"
    f"{clean_stats['variance']:>20.3f}"
)

print(
    f"{'СКО, мс':<25}"
    f"{original_stats['std_dev']:>15.3f}"
    f"{with_outliers_stats['std_dev']:>18.3f}"
    f"{clean_stats['std_dev']:>20.3f}"
)


# ============================================================
# 10. ГРАФИК ДОБАВЛЕННЫХ ВЫБРОСОВ
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(
    range(1, len(measurements_with_outliers) + 1),
    measurements_with_outliers,
    marker="o",
    markersize=3,
    linewidth=1
)

plt.axhline(
    upper_bound,
    linestyle="--",
    label=f"Верхняя граница = {upper_bound:.2f} мс"
)

plt.title("Выборка с искусственно добавленными выбросами")
plt.xlabel("Номер измерения")
plt.ylabel("Задержка, мс")

plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


# ============================================================
# 11. ГРАФИК ПОСЛЕ УДАЛЕНИЯ ВЫБРОСОВ
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(
    range(1, len(clean_measurements) + 1),
    clean_measurements,
    marker="o",
    markersize=3,
    linewidth=1
)

plt.axhline(
    clean_stats["mean"],
    linestyle="--",
    label=f"Среднее = {clean_stats['mean']:.2f} мс"
)

plt.title("Выборка после удаления выбросов")
plt.xlabel("Номер измерения")
plt.ylabel("Задержка, мс")

plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


# ============================================================
# 12. АВТОМАТИЧЕСКИЙ ВЫВОД
# ============================================================

print("\nАНАЛИЗ РЕЗУЛЬТАТОВ")
print("-" * 60)

print(
    f"До добавления выбросов среднее значение составляло "
    f"{original_stats['mean']:.3f} мс."
)

print(
    f"После добавления выбросов среднее изменилось до "
    f"{with_outliers_stats['mean']:.3f} мс."
)

print(
    f"После удаления обнаруженных выбросов среднее составило "
    f"{clean_stats['mean']:.3f} мс."
)

print(
    f"\nСКО до добавления выбросов: "
    f"{original_stats['std_dev']:.3f} мс."
)

print(
    f"СКО с выбросами: "
    f"{with_outliers_stats['std_dev']:.3f} мс."
)

print(
    f"СКО после удаления выбросов: "
    f"{clean_stats['std_dev']:.3f} мс."
)

print(
    "\nВывод: искусственные аномальные значения существенно "
    "увеличивают разброс результатов и могут смещать среднее."
    " Предварительная обработка результатов измерений позволяет "
    "уменьшить влияние выбросов и получить более устойчивые "
    "статистические оценки."
)