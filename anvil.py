from collections import defaultdict

def min_coins(target, coins):
    """ Возвращает минимальное количество монет для суммы target и все варианты разложения. """

    # DP-массив для хранения минимального количества монет для каждой суммы
    dp = {0: (0, [[]])}  # {сумма: (минимальное количество монет, список всех вариантов)}

    for value in range(1, target + 1):
        min_count = float('inf')
        best_ways = []

        for coin in coins:
            prev_value = value - coin
            if prev_value in dp:
                prev_count, prev_ways = dp[prev_value]
                new_count = prev_count + 1

                if new_count < min_count:
                    min_count = new_count
                    best_ways = [way + [coin] for way in prev_ways]  # Обновляем лучший вариант
                elif new_count == min_count:
                    best_ways.extend([way + [coin] for way in prev_ways])  # Добавляем равновесный вариант

        if best_ways:
            dp[value] = (min_count, best_ways)

    return dp.get(target, (float('inf'), []))[1]  # Возвращаем только список разложений

# === Жестко заданные номиналы ===
coins = [-15, -6, -3, 2, 7, 13, 16]

# === Число, которое нужно разложить ===
target = 6

# === Запуск алгоритма ===
solutions = min_coins(target, coins)

# === Вывод результатов ===
if solutions:
    print(f"Минимальное количество монет: {len(solutions[0])}")
    print("Все возможные разложения:")
    for solution in solutions:
        print(sorted(solution))  # Выводим отсортированные разложения
else:
    print("Невозможно разложить заданное число этими номиналами.")
