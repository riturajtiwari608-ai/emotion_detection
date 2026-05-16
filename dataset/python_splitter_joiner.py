import csv
from pathlib import Path

ENCODING = "utf-8"


def find_csv_files():
    """
    Find all CSV files in current directory.
    Excludes already split files like *_part1.csv
    """
    files = []

    for f in Path(".").glob("*.csv"):
        name = f.stem.lower()

        if (
            name.endswith("_part1")
            or name.endswith("_part2")
            or name.endswith("_part3")
        ):
            continue

        files.append(f)

    return sorted(files)


def find_split_groups():
    """
    Auto-detect split CSV groups.
    Example:
        data_part1.csv
        data_part2.csv
        data_part3.csv
    """

    groups = {}

    for f in Path(".").glob("*_part*.csv"):
        stem = f.stem

        if stem.endswith("_part1"):
            base = stem[:-6]
            groups.setdefault(base, {})["1"] = f

        elif stem.endswith("_part2"):
            base = stem[:-6]
            groups.setdefault(base, {})["2"] = f

        elif stem.endswith("_part3"):
            base = stem[:-6]
            groups.setdefault(base, {})["3"] = f

    valid = {}

    for base, parts in groups.items():
        if all(k in parts for k in ("1", "2", "3")):
            valid[base] = parts

    return valid


def count_data_rows(csv_path: Path) -> int:
    with open(csv_path, "r", newline="", encoding=ENCODING) as f:
        reader = csv.reader(f)

        next(reader, None)  # skip header

        return sum(1 for _ in reader)


def split_csv_into_three(csv_path: Path):
    total_rows = count_data_rows(csv_path)

    if total_rows == 0:
        print("CSV has no data rows.")
        return

    base, extra = divmod(total_rows, 3)

    quotas = [base + (1 if i < extra else 0) for i in range(3)]

    output_files = [
        csv_path.parent / f"{csv_path.stem}_part1.csv",
        csv_path.parent / f"{csv_path.stem}_part2.csv",
        csv_path.parent / f"{csv_path.stem}_part3.csv",
    ]

    print(f"\nSplitting: {csv_path.name}")
    print(f"Total rows: {total_rows}")
    print(f"Distribution: {quotas}")

    handles = []
    writers = []

    try:
        with open(csv_path, "r", newline="", encoding=ENCODING) as src:
            reader = csv.reader(src)

            header = next(reader)

            for out in output_files:
                h = open(out, "w", newline="", encoding=ENCODING)

                handles.append(h)

                w = csv.writer(h)

                w.writerow(header)

                writers.append(w)

            current_part = 0
            written = 0

            for row in reader:

                while written >= quotas[current_part]:
                    current_part += 1
                    written = 0

                writers[current_part].writerow(row)

                written += 1

    finally:
        for h in handles:
            h.close()

    print("\nCreated:")
    for f in output_files:
        print(f"  - {f.name}")


def join_csv_parts(base_name, parts):
    output_file = Path(f"{base_name}.csv")

    print(f"\nJoining group: {base_name}")

    with open(output_file, "w", newline="", encoding=ENCODING) as out_f:

        writer = csv.writer(out_f)

        header_written = False
        first_header = None

        for idx in ("1", "2", "3"):

            with open(parts[idx], "r", newline="", encoding=ENCODING) as f:

                reader = csv.reader(f)

                header = next(reader, None)

                if header is None:
                    continue

                if not header_written:
                    writer.writerow(header)

                    first_header = header

                    header_written = True

                else:
                    if header != first_header:
                        raise ValueError(f"Header mismatch in {parts[idx].name}")

                for row in reader:
                    writer.writerow(row)

    print(f"Created: {output_file.name}")


def choose_from_list(items, title):
    print(f"\n{title}")

    for i, item in enumerate(items, start=1):
        print(f"{i}. {item}")

    while True:
        try:
            choice = int(input("\nSelect number: "))

            if 1 <= choice <= len(items):
                return items[choice - 1]

        except ValueError:
            pass

        print("Invalid selection.")


def menu():

    while True:

        print("\n==============================")
        print(" CSV Split / Join Utility")
        print("==============================")
        print("1. Split CSV into 3 parts")
        print("2. Join split CSV files")
        print("3. Exit")

        choice = input("\nEnter choice: ").strip()

        if choice == "1":

            csv_files = find_csv_files()

            if not csv_files:
                print("\nNo CSV files found.")
                continue

            selected = choose_from_list(
                [f.name for f in csv_files], "Available CSV files:"
            )

            split_csv_into_three(Path(selected))

        elif choice == "2":

            groups = find_split_groups()

            if not groups:
                print("\nNo split CSV groups found.")
                continue

            selected = choose_from_list(list(groups.keys()), "Detected split groups:")

            try:
                join_csv_parts(selected, groups[selected])

            except Exception as e:
                print(f"\nError: {e}")

        elif choice == "3":
            print("\nGoodbye.")
            break

        else:
            print("\nInvalid choice.")


if __name__ == "__main__":
    menu()
