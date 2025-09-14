import json
from datetime import datetime


def load_jsonl_file(file_path):
    data = []
    with open(file_path, 'r') as infile:
        for line in infile:
            d = json.loads(line)
            data.append(d)
    return data

def get_syz_time(data, time_limit):
    result = []
    fmt = "%Y-%m-%d %H:%M"
    for single_bug in data:
        discussions = single_bug.get('mails', {})
        if 'mails' in discussions:
            discussions = discussions['mails']
        
        for discussion in discussions:
            if discussion.get('num', 0) <= 1:
                continue
            mail_list = discussion.get('mail_list', [])
        times = [mail['date'] for mail in mail_list if 'date' in mail]
        time = datetime.strptime(times[0], fmt)
        if time > time_limit:
            result.append(single_bug)
    return result


def get_bugzilla_time(data, time_limit):
    result = []
    fmt = "%Y-%m-%d %H:%M:%S %Z" 
    for single_bug in data:
        times = single_bug.get('times', [])
        time = datetime.strptime(times[0], fmt)
        if time > time_limit:
            result.append(single_bug)
    return result
    
    
def filter_time(syz_data, bugzilla_data, time_limit):
    time_limit = datetime.strptime(time_limit, "%Y-%m-%d")
    syz_result = get_syz_time(syz_data, time_limit)
    bugzilla_result = get_bugzilla_time(bugzilla_data, time_limit)
    print(f"syz data count: {len(syz_result)}")
    print(f"bugzilla data count: {len(bugzilla_result)}")
    return syz_result, bugzilla_result
    
       
if __name__ == "__main__":
    time_limit = "2024-07-01"
    filter_time(time_limit)