file_path = input()

with open(file_path, "r") as file:
    lines = file.readlines()
    count = 0
    for line in lines:
        count += 1
        if len(line) > 79:
            print(f"Line {count}: S001 Too long")
