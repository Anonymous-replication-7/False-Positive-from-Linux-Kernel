import sys
import os

from root_cause import root_cause_standard
sys.path.append(os.path.abspath("analyse/rq2"))

from rq2_component import load_data
from data.config import bugzilla_mapping, syzkaller_mapping, bugzilla_data_file, syzkaller_data_file
# from root_cause import root_cause_dict
import json
import re



def get_component_dict():
    bugzilla_data = load_data(bugzilla_data_file)
    syzkaller_data = load_data(syzkaller_data_file)

    todo_names = ['bugzilla', 'syzbot']
    todo_data = [bugzilla_data, syzkaller_data]
    bguzilla_result = {}
    syz_result = {}
    for name, data in zip(todo_names, todo_data):
        
        print(f"Processing {name} data...")
        for item in data:
            label_type = item.get('label_type', 'unknown')
            if label_type != 'fp':
                continue
            if name == "bugzilla":
                component = item["component"].split("(")[0].strip() if item['component'] else "unknown" 
                subsystem = bugzilla_mapping.get(component, "unknown")
                bguzilla_result[item['url']] = subsystem

            elif name == "syzbot":
                component = item['subsystems'][0]['name'] if item['subsystems'] else "unknown" 
                subsystem = syzkaller_mapping.get(component, "unknown")
                syz_result[item['url']] = subsystem
    return bguzilla_result, syz_result
        
def get_root_cause_dict():
    bugzilla_result = {}
    syz_result = {}
    with open("data/bugzilla_data.jsonl", 'r') as infile:
        for line in infile:
            d = json.loads(line)
            if d['label_type'] == 'fp':
                bugzilla_result[d['url']] = root_cause_standard(d['root_cause'])
    
    with open("data/syzkaller_data.jsonl", 'r') as infile:
        for line in infile:
            d = json.loads(line)
            if d['label_type'] == 'fp':
                syz_result[d['url']] = root_cause_standard(d['root_cause'])
    return bugzilla_result, syz_result

def merge_jsonl_data(data1, data2):
    merged_data = {}
    components = ["File System", "Drivers", "Networking", "Kernel Core", "Tools","Security", "IO/Storage"]

    for data in [data1, data2]:
        for component, causes in data.items():
            if component not in merged_data and component in components:
                merged_data[component] = {}
            if component in components:
                for cause, count in causes.items():
                    if cause not in merged_data[component]:
                        merged_data[component][cause] = 0

                    merged_data[component][cause] += count

    return merged_data

def combine_data():
    bguzilla_cp, syz_cp = get_component_dict()
    bugzilla_rc, syz_rc = get_root_cause_dict()
    bugzilla_combine_dict = {}
    for key, value in bguzilla_cp.items():
        if key in bugzilla_rc:
            component = value
            root_cause = bugzilla_rc[key]
            if component not in bugzilla_combine_dict:
                bugzilla_combine_dict[component] = {}
            if root_cause not in bugzilla_combine_dict[component]:
                bugzilla_combine_dict[component][root_cause] = 0
            bugzilla_combine_dict[component][root_cause] += 1

    syz_combine_dict = {}
    for key, value in syz_cp.items():
        if key in syz_rc:
            component = value
            root_cause = syz_rc[key]
            if component not in syz_combine_dict:
                syz_combine_dict[component] = {}
            if root_cause not in syz_combine_dict[component]:
                syz_combine_dict[component][root_cause] = 0
            syz_combine_dict[component][root_cause] += 1

    from collections import OrderedDict
    bugzilla_combine_dict = OrderedDict(sorted(bugzilla_combine_dict.items(), key=lambda x: x[0]))
    syz_combine_dict = OrderedDict(sorted(syz_combine_dict.items(), key=lambda x: x[0]))

    with open('analyse/rq3/data/all_component_root_cause.json', 'w') as outfile:
        json.dump(merge_jsonl_data(bugzilla_combine_dict, syz_combine_dict), outfile, indent=4)

    merge_percent = {}
    merge = merge_jsonl_data(bugzilla_combine_dict, syz_combine_dict)
    for component, causes in merge.items():
        total = sum(causes.values())
        merge_percent[component] = {
            cause: round((count / total) * 100, 2) for cause, count in causes.items()
        }
    import pandas as pd
    merge_percent = pd.DataFrame(merge_percent).fillna(0)
    merge_df = pd.DataFrame(merge).fillna(0)

    merge_percent.T.to_csv("analyse/rq3/data/all_root_cause_percent.csv", encoding="utf-8-sig")
    merge_df.T.to_csv("analyse/rq3/data/all_root_cause_counts.csv", encoding="utf-8-sig")

    with open(f'analyse/rq3/data/all_component_root_cause.json', 'w') as outfile:
        json.dump(merge, outfile, indent=4)


if __name__ == "__main__":
    combine_data()
