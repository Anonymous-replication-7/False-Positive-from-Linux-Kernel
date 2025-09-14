
import json
from data.config import bugzilla_mapping, syzkaller_mapping, bugzilla_data_file, syzkaller_data_file


def load_data(file_path: str):
    data = []
    with open(file_path, 'r') as infile:
        for line in infile:
            d = json.loads(line)
            data.append(d)
    return data

def count():
    bugzilla_data = load_data(bugzilla_data_file)
    syzkaller_data = load_data(syzkaller_data_file)

    todo_names = ['bugzilla', 'syzbot']
    todo_data = [bugzilla_data, syzkaller_data]

    for name, data in zip(todo_names, todo_data):
        result = {}
        print(f"Processing {name} data...")
        for item in data:
            label_type = item.get('label_type', 'unknown')
            if label_type != 'fp':
                continue
            if name == "bugzilla":
                component = item["component"].split("(")[0].strip() if "component" in item else "unknown1"
                subsystem = bugzilla_mapping.get(component, "unknown2")

            elif name == "syzbot":
                component = item['subsystems'][0]['name'] if item['subsystems'] else "unknown"
                subsystem = syzkaller_mapping.get(component, "unknown")

            result[subsystem] = result.get(subsystem, 0) + 1

        # sourt by key
        result = dict(sorted(result.items(), key=lambda x: x[0], reverse=True))
        if name == "bugzilla":
            with open('analyse/rq2/data/bugzilla_components_result.json', 'w') as outfile:
                json.dump(result, outfile, indent=4)
        elif name == "syzbot":
            with open('analyse/rq2/data/syzkaller_components_result.json', 'w') as outfile:
                json.dump(result, outfile, indent=4)

        for component, count in result.items():
            print(f"{component}: {count}")
        
        print('=' * 50)

        
count()