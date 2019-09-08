import argparse
import os
import sys
from autotimer import AutoTimer
import subprocess
import project_handler as projectHandler 
class ArgsHandler(): 

    def __init__(self):
        # Load Projects
        projectHandler.get_projects()

        parser = argparse.ArgumentParser(
            description='Pretends to be git',
            usage='''autotimer <command> [<args>]

                The most commonly used autotimer commands are:
                new        Create a New Project
                start      Start Tracking an Existent Project 
                delete     Delete A project and its history
                list       Show all existent projects
                ''')

        parser.add_argument('command', help='Subcommand to run')
        
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2]) 
        
        if not hasattr(self, args.command):
            print( 'Unrecognized command')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def new(self):
        parser = argparse.ArgumentParser(
            description='Create  a New Project')
        # prefixing the argument with -- means it's optional
        parser.add_argument('project_name', help='Name of the New Project')
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        args = parser.parse_args(sys.argv[2:])
        create_project(args.project_name)

    def delete(self):
        parser = argparse.ArgumentParser(
            description='Delete A Project')
        # NOT prefixing the argument with -- means it's not optional
        parser.add_argument('project')
        args = parser.parse_args(sys.argv[2:])
        delete_project(args.project)

    def start(self):
        global runningProjects
        global projects
        parser = argparse.ArgumentParser(
            description='Start Tracking A Project')
        # NOT prefixing the argument with -- means it's not optional
        parser.add_argument('project')
        parser.add_argument('-O', '--output', nargs='+', choices=['activities', 'logs', 'overview'])
        parser.add_argument('--fg', action='store_true')

        args = parser.parse_args(sys.argv[2:])
        projectHandler.get_projects()
        # Verificar si el proyecto existe
        exists = False
        for project in projectHandler.projects: 
            if project['name'] == args.project:
                exists = True
        for project in projectHandler.runningProjects: 
            if project['project'] == args.project:
                return print('Already running')
        
        if not exists:
            return print(f"No such project named: {args.project}")
        
        output_srt = ''
        if args.output and not args.fg:
            output_srt = '--output '+ " ".join(args.output) 
                

        # The Magic Starts
        if args.fg:
            output = {
                'activities':False,
                'logs':False,
                'overview':True
            }
            if args.output:
                for o in args.output:
                    output[o] = True; 
            projectHandler.runningProjects.append({
            "pid": os.getpid(),
            "project": args.project
            }) 
            projectHandler.save_project_info()
            timer = AutoTimer(output=output) 
            timer.start_timer(args.project)
        else:
            print(output_srt)
            subprocess.call(f'nohup python3 ./timer.py {args.project} {output_srt} &', shell=True) 

    def list_running(self):
        global runningProjects
        parser = argparse.ArgumentParser(
            description='Download objects and refs from another repository')
        # NOT prefixing the argument with -- means it's not optional
        # parser.add_argument('repository')
        # args = parser.parse_args(sys.argv[2:]) 
        projectHandler.get_projects()
        if not projectHandler.runningProjects:
            print('No projects running')
        for log in projectHandler.runningProjects: 
            print(f'{log["pid"]} - {log["project"]}')
        
    def list(self):
        global projects
        parser = argparse.ArgumentParser(
            description='Download objects and refs from another repository')
        # NOT prefixing the argument with -- means it's not optional
        # parser.add_argument('repository')
        # args = parser.parse_args(sys.argv[2:]) 
        count = 0;
        projectHandler.get_projects()
        if not projectHandler.projects:
            print('No projects yet')
        for project in projectHandler.projects:
            count = count + 1
            print(f'{count} - {project["name"]}')

    def stop(self): 
        parser = argparse.ArgumentParser(
            description='Download objects and refs from another repository')
        # NOT prefixing the argument with -- means it's not optional
        parser.add_argument('project')
        args = parser.parse_args(sys.argv[2:]) 

        count = 0;
        projectHandler.get_projects() 
        for i in range(len(projectHandler.runningProjects)):
            if projectHandler.runningProjects[i]["project"] == args.project:
                subprocess.call(f"kill {projectHandler.runningProjects[i]['pid']}", shell=True)
                del projectHandler.runningProjects[i]
                return projectHandler.save_project_info()
        print('No projects running') 