import os
import json
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu

# # Cliff's Delta implementation
def cliffs_delta(x, y):
    x = np.array(x)
    y = np.array(y)
    n_x = len(x)
    n_y = len(y)
    gt = sum(xx > yy for xx in x for yy in y)
    lt = sum(xx < yy for xx in x for yy in y)
    delta = (gt - lt) / (n_x * n_y)
    return delta

# Outlier removal with IQR
def remove_outliers(data):
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return [x for x in data if lower <= x <= upper]

# from analyse.rq1.conf import syz_data_file, bugzilla_data_file

syz_data_file = "data/syzkaller_data.jsonl"
bugzilla_data_file = "data/bugzilla_data.jsonl"

def load_jsonl_file(file_path):
    """Load a JSON Lines file and return a list of dictionaries."""
    with open(file_path, 'r') as file:
        return [json.loads(line) for line in file]


def calculate_time_span(time_list,name):
    fmt = "%Y-%m-%d %H:%M:%S %Z" if name == "bugzilla" else "%Y-%m-%d %H:%M"
     # parse times and sort
    parsed_times = sorted([datetime.strptime(t, fmt) for t in time_list])
    
    # calculate time span, convert to hours
    time_span = parsed_times[-1] - parsed_times[0]
    hours = time_span.total_seconds() / 3600
    log_hours = np.log10(hours)
    return log_hours


def draw_box_plot(bugzilla_fp, bugzilla_tp, syz_fp, syz_tp, res_path):
    # Prepare data for plotting
    labels = ['bugzilla', 'syzkaller']

    # Example: clean each list
    bugzilla_fp_clean = bugzilla_fp
    bugzilla_tp_clean = bugzilla_tp
    syz_fp_clean = syz_fp
    syz_tp_clean = syz_tp

    fp_tp_data = [
        [bugzilla_fp_clean, bugzilla_tp_clean],
        [syz_fp_clean, syz_tp_clean]
    ]

    # Positions for nested boxes
    positions = [[1, 1.3], [2, 2.3]]

    # Colors for fp and tp
    colors = ['#e29d95', '#8dc394']

    # Create boxplot without outliers (showfliers=False)
    fig, ax = plt.subplots(figsize=(6, 6))

    for i, (fp, tp) in enumerate(fp_tp_data):
        bplot = ax.boxplot([fp, tp],
                        positions=positions[i],
                        widths=0.25,
                        patch_artist=True,
                        labels=['', ''],
                        showfliers=False,  
                        medianprops=dict(color='black', linewidth=1, linestyle='-'),
                        meanline=True) # add mean line) 
        for patch, color in zip(bplot['boxes'], colors):
            patch.set_facecolor(color)
    ax.set_xticks([1.15, 2.15])
    ax.set_xticklabels(labels, fontsize=24)
    ax.tick_params(axis='y', labelsize=20)
    from matplotlib.ticker import MaxNLocator
    from matplotlib.ticker import MultipleLocator
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt_title = ""
    if "all_authors" in res_path:
        plt_title = "Number of Participants"
        ax.yaxis.set_major_locator(MultipleLocator(2))
    elif "all_comments" in res_path:
        plt_title = "Number of Comments"
        ax.yaxis.set_major_locator(MultipleLocator(4))

    plt.title(plt_title, fontsize=24, fontweight='bold', pad=25)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()  
    plt.savefig(res_path, bbox_inches='tight', dpi=300)


def get_syz_statistics(single_bug):
    discussions = single_bug.get('mails', {})
    if 'mails' in discussions:
        discussions = discussions['mails']
    time_diffs = []
    comments = []
    authors = set()

    processed_discussions = set()
    
    for discussion in discussions:
        if discussion.get('num', 0) <= 1:
            continue
        mail_list = discussion.get('mail_list', [])
        
        all_contents = [mail['content'] for mail in mail_list]
        discussion_content = '\n'.join(all_contents)
        
        if discussion_content in processed_discussions:
            continue
        
        processed_discussions.add(discussion_content)
        
        # collect comments if they exist
        comments.extend(mail_list)
        
        # collect authors
        authors.update(mail['sender'] for mail in mail_list)
        
        # collect dates
        times = [mail['date'] for mail in mail_list if 'date' in mail]
        if times:
            time_diffs.append(calculate_time_span(times, 'syz'))

    if not time_diffs:
        return None, None, None, None

    mean_diff = sum(time_diffs) / len(time_diffs)
    sum_diff = sum(time_diffs)
    return mean_diff, sum_diff, comments, list(authors)


def get_bugzilla_statistics(single_bug):
    times = single_bug.get('times', [])
    comments = single_bug.get('comments', [])
    authors = list(set(single_bug['authors']))
    time_diff = calculate_time_span(times, 'bugzilla')
    if not time_diff:
        return None, None, None, None
    return time_diff, time_diff, comments, authors
    

def process_row_statistic(todo_data):
    res_dict = {key: [] for key in todo_data}
    
    for data_type, data in todo_data.items():
        analyse_func = get_syz_statistics if data_type == 'syz' else get_bugzilla_statistics
            
        for single_bug in data:
            single_res = {}
            mean_time_diff, sum_time_diff, all_comments, all_authors = analyse_func(single_bug)
            if not mean_time_diff:
                continue
            single_res = {
                    'link': single_bug.get('url'),
                    'type': single_bug.get('label_type'),
                    'data_type': single_bug.get('data_type', ''),
                    'mean_time_diff': mean_time_diff,
                    'sum_time_diff': sum_time_diff,
                    'all_comments': len(all_comments),
                    'all_authors': len(all_authors)
            }
            res_dict[data_type].append(single_res)
    return res_dict

    

if __name__ == "__main__":
    syz_data = load_jsonl_file(syz_data_file)
    bugzilla_data = load_jsonl_file(bugzilla_data_file)

    todo_data = {
        'syz': syz_data,
        'bugzilla': bugzilla_data
    }

    res_dict = process_row_statistic(todo_data)

    for res_type in ['sum_time_diff', 'all_comments', 'all_authors']:
        print('=' * 30)
        print(f"Results for {res_type}:")
        bugzilla_fp = [bug[res_type] for bug in res_dict['bugzilla'] if bug['type'] == 'fp']
        bugzilla_tp = [bug[res_type] for bug in res_dict['bugzilla'] if bug['type'] == 'tp']
        syz_fp = [bug[res_type] for bug in res_dict['syz'] if bug['type'] == 'fp']
        syz_tp = [bug[res_type] for bug in res_dict['syz'] if bug['type'] == 'tp']
        
        res_path = f'analyse/rq1/results_plt/{res_type}.png'
        
        os.makedirs(os.path.dirname(res_path), exist_ok=True)
        draw_box_plot(bugzilla_fp, bugzilla_tp, syz_fp, syz_tp, res_path)
        print('=' * 30)
        print(res_type)
        print(f"mean bugzilla_fp: {np.mean(bugzilla_fp)}, median: {np.median(bugzilla_fp)}")
        print(f"mean bugzilla_tp: {np.mean(bugzilla_tp)}, median: {np.median(bugzilla_tp)}")
        print(f"mean syz_fp: {np.mean(syz_fp)}, median: {np.median(syz_fp)}")
        print(f"mean syz_tp: {np.mean(syz_tp)}, median: {np.median(syz_tp)}")


        bugzilla_fp_clean = remove_outliers(bugzilla_fp)
        bugzilla_tp_clean = remove_outliers(bugzilla_tp)
        syz_fp_clean = remove_outliers(syz_fp)
        syz_tp_clean = remove_outliers(syz_tp)


        bugzilla_fp_clean = bugzilla_fp
        bugzilla_tp_clean = bugzilla_tp
        syz_fp_clean = syz_fp
        syz_tp_clean = syz_tp

        results = {}
        for name, fp, tp in [
            ("Bugzilla", bugzilla_fp_clean, bugzilla_tp_clean),
            ("Syzkaller", syz_fp_clean, syz_tp_clean)
        ]:
            u_stat, p_val = mannwhitneyu(fp, tp, alternative='two-sided')
            delta = cliffs_delta(fp, tp)
            # delta = cliffs_delta(fp, tp)
            results[name] = {
                "Mann-Whitney U": u_stat,
                "p-value": p_val,
                "Cliff's Delta": delta
            }

        print(results)