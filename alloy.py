import argparse
from itertools import product

def calculate_alloy(ingots, proportions, granularity):
    total_mb = ingots * 144
    min_values = {comp: (total_mb * pct[0]) // 100 for comp, pct in proportions.items()}
    max_values = {comp: (total_mb * pct[1]) // 100 for comp, pct in proportions.items()}
    
    min_values = {comp: (val // granularity) * granularity for comp, val in min_values.items()}
    max_values = {comp: (val // granularity) * granularity for comp, val in max_values.items()}
    
    valid_combinations = [
        combo for combo in product(
            *(range(min_values[comp], max_values[comp] + 1, granularity) for comp in proportions)
        ) if sum(combo) == total_mb
    ]
    
    if not valid_combinations:
        print("Невозможно создать сплав с заданными параметрами.")
        return
    
    print("Возможные комбинации компонентов:")
    for combo in valid_combinations:
        result = {comp: amount for comp, amount in zip(proportions.keys(), combo)}
        print(result)

def main():
    parser = argparse.ArgumentParser(description="Расчёт количества компонентов сплава в mb.")
    parser.add_argument("ingots", type=int, help="Количество слитков")
    parser.add_argument("alloy", type=str, help="Название сплава")
    parser.add_argument("--granularity", type=int, default=16, help="Значение кратности (по умолчанию 16)")
    args = parser.parse_args()
    
    alloys = {
        "Bismuth Bronze": {
            "Copper": (50, 65),
            "Zinc": (20, 30),
            "Bismuth": (10, 20),
        },
        "Black Bronze": {
            "Copper": (50, 70),
            "Gold": (10, 25),
            "Silver": (10, 25),
        },
        "Bronze": {
            "Copper": (88, 92),
            "Tin": (8, 12),
        },
        "Brass": {
            "Copper": (88, 92),
            "Zinc": (8, 12),
        },
    }
    
    if args.alloy not in alloys:
        print("Неизвестный сплав. Доступные сплавы:", ", ".join(alloys.keys()))
        return
    
    calculate_alloy(args.ingots, alloys[args.alloy], args.granularity)
    
if __name__ == "__main__":
    main()
