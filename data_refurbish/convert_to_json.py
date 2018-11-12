from json import loads, dump

def convert_to_json(source, target):
    linecount = get_lines_in_file(source)
    courser = 0
    current_line = '[\n'
    with open(source, 'r') as s:
        for line in s:
            if courser < linecount:
                current_line = current_line + ('  ' + line + ',')
            else:
                current_line = current_line + ('  ' + line)
            with open(target, 'a') as t:
                dump(current_line, t)
            courser += 1
            current_line = ''


def get_lines_in_file(filename):
    return sum(1 for line in open(filename))


def convert_to_json2(source, target):
    result = []
    with open(source, 'r') as s:
        for line in s:
            result.append(loads(line))
    with open(target, 'a') as t:
        dump(result, t)


convert_to_json2('../data/final/Repo_Commits', '../data/final/Repo_Commits_JSON.json')
