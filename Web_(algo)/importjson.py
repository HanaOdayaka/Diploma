import json

def imports(robots_file, plants_file):
    robots_cells = []
    plants_cells = []

    data = json.loads(robots_file)

    for i in data['record']['robots']:
        tasks = [str(task)+'\n' for task in  i['tasks']]
        str_tasks =''
        for j in range(len(tasks)):
            str_tasks += tasks[j]
            if j+1 != len(tasks):
                str_tasks += '-------------------------------'
                str_tasks += '\n'

        robots_cells.append((str(i['robot_name']), str(i['battery']), str_tasks))

    data = json.loads(plants_file)

    for i in data['record']['plants']:
        plants_cells.append((str(i['plant_name']), str(i['status'])))

    return tuple(robots_cells), tuple(plants_cells)
