import json

projects = []
runningProjects = []

def save_project_info():
    with open('projects.json', 'w') as json_file:
        json.dump({
            'projects': projects,
            'running': runningProjects
        }, json_file, indent=4, sort_keys=True)
    

def get_projects():
    global projects, runningProjects
    try:
        with open('projects.json', 'r') as f:
            data = json.load(f) 
            projects = data['projects']
            runningProjects = data['running']  
    except Exception:
        print('No Projects Added')
    finally:
        return projects


def create_project(project_name):
    global projects
    for project in projects:
        if project_name == project['name']:
            return print('Error: Already exists a project named like this: check running --projects flag')
    projects.append({
        'name': project_name,
        'id': len(projects)
    })
    save_project_info()
    with open(f'projects/{project_name}.json', 'w') as project_file:
        json.dump({}, project_file) 
    return  projects

def delete_project(project_name):
    answer = input(f'Sure you wanna delete project: {project_name}? (Y/n): ')
    if answer.lower() == 'y':
        for i in range(len(projects)):
            project = projects[i]
            if project_name == project['name']:
                os.remove(f'projects/{project_name}.json')
                del projects[i]
                return save_project_info()
        print(f'No project named : {project_name}')
