import argparse
import os
from autotimer import AutoTimer
import project_handler as projectHandler

parser = argparse.ArgumentParser()
parser.add_argument('project')
parser.add_argument('-O', '--output', nargs='+', choices=['activities', 'logs', 'overview'])

args = parser.parse_args()

print("Initialized From Timer CLI")
projectHandler.get_projects()
projectHandler.runningProjects.append({
    "pid": os.getpid(),
    "project": args.project
})
projectHandler.save_project_info()

output = {
    'activities':False,
    'logs':False,
    'overview':True
}
if args.output:
    for o in args.output:
        output[o] = True; 
timer = AutoTimer(output=output)
timer.start_timer(args.project)