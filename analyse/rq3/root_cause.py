import json
import re


def root_cause_standard(root_cause):
    if "Hardware Environment Configuration" in root_cause  or "Software Environment Configuration" in root_cause:
        return "1. Incorrect Environment Configuration"
    elif "Unsupported Invocation" in root_cause or "Inappropriate Report Place" in root_cause or "Incorrect Operation" in root_cause:  
        return "2. Incorrect Usage"
    elif "Limitation Unawareness" in root_cause or "Semantic Misunderstanding" in root_cause or "Implicit Behaviour Misunderstanding" in root_cause:
        return "3. Misunderstanding of Features or Limitations"
    elif "Hardware Issues" in root_cause or "Userspace Dependency Issues" in root_cause or "Outdated Firmware or Firmware Issues" in root_cause:
        return "External Dependency Issues"
    elif "Typo" in root_cause:
        return "5. Typo"
    else:  
        return root_cause
        



def get_root_cause(need_sub):
    bugzilla_rc = {}
    syz_rc = {}
    with open("data/bugzilla_data.jsonl", 'r') as infile:
        for line in infile:
            d = json.loads(line)
            if d['label_type'] == 'fp':
                bugzilla_rc[d['url']] = d['root_cause']
    
    with open("data/syzkaller_data.jsonl", 'r') as infile:
        for line in infile:
            d = json.loads(line)
            if d['label_type'] == 'fp':
                syz_rc[d['url']] = d['root_cause']

    from collections import OrderedDict
    bugzilla_rc = OrderedDict(sorted(bugzilla_rc.items(), key=lambda x: x[0]))
    syz_rc = OrderedDict(sorted(syz_rc.items(), key=lambda x: x[0]))

    if need_sub:
        with open("analyse/rq3/data/bugzilla_rc_sub.json", 'w') as outfile:
            json.dump(bugzilla_rc, outfile, indent=4)
        with open("analyse/rq3/data/syz_rc_sub.json", 'w') as outfile:
            json.dump(syz_rc, outfile, indent=4)
    else:
        with open("analyse/rq3/data/bugzilla_rc.json", 'w') as outfile:
            json.dump(bugzilla_rc, outfile, indent=4)
        with open("analyse/rq3/data/syz_rc.json", 'w') as outfile:
            json.dump(syz_rc, outfile, indent=4)


if __name__ == "__main__":
    get_root_cause(True)
    get_root_cause(False)

