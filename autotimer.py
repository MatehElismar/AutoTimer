#!/usr/bin/env python3
from __future__ import print_function
import time
from os import system
from activity import *
import json
import datetime
import sys
import settings
if sys.platform in ['Windows', 'win32', 'cygwin']:
    import win32gui
    import uiautomation as auto
elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
    from AppKit import NSWorkspace
    from Foundation import *
elif sys.platform in ['linux', 'linux2']:
        import linux as l



class AutoTimer():
    def __init__(self, output = {
            'activities':False,
            'logs':False,
            'overview':True
        }):

        self.active_window_name = ""
        self.activity_name = ""
        self.start_time = datetime.datetime.now()
        self.activeList = AcitivyList([], [], []) 
        
        self.output = output
        print(f'output : {output}')

    def url_to_name(self, url):
        string_list = url.split('/')
        return string_list[2]


    def get_active_window(self):
        _active_window_name = None
        # windows
        if sys.platform in ['Windows', 'win32', 'cygwin']:
            window = win32gui.GetForegroundWindow()
            _active_window_name = win32gui.GetWindowText(window)
        # MAC
        elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
            _active_window_name = (NSWorkspace.sharedWorkspace()
                                .activeApplication()['NSApplicationName'])
        else:
            print("sys.platform={platform} is not supported."
                .format(platform=sys.platform))
            print(sys.version)
        return _active_window_name


    def get_chrome_url(self):
        if sys.platform in ['Windows', 'win32', 'cygwin']:
            window = win32gui.GetForegroundWindow()
            chromeControl = auto.ControlFromHandle(window)
            edit = chromeControl.EditControl()
            return 'https://' + edit.GetValuePattern().Value 
        elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
            textOfMyScript = """tell app "google chrome" to get the url of the active tab of window 1"""
            s = NSAppleScript.initWithSource_(
                NSAppleScript.alloc(), textOfMyScript)
            results, err = s.executeAndReturnError_(None)
            return results.stringValue()
        else:
            print("sys.platform={platform} is not supported."
                .format(platform=sys.platform))
            print(sys.version)
        return _active_window_name

    
    def start_timer(self, project_name): 

        try:
            self.activeList = self.activeList.initialize_me(project_name)  
        except Exception:
            print('No JSON DATA FOUND')

        try:
            print('Tracking Time on Project: ' + project_name)

            first_time = True
            # Main Code 
            while True:
                previous_site = ""
                if sys.platform not in ['linux', 'linux2']:
                    new_window_name = get_active_window()
                    if 'Google Chrome' in new_window_name:
                        new_window_name = url_to_name(get_chrome_url())
                if sys.platform in ['linux', 'linux2']:
                    new_window_name = l.get_active_window_x()
                    for browser in settings.BROWSERS:
                        if browser in new_window_name:
                            new_window_name = l.get_chrome_url_x()
                            break;

                
                if self.active_window_name != new_window_name:
                    print(self.active_window_name)
                    self.activity_name = self.active_window_name

                    if not first_time:
                        end_time = datetime.datetime.now()
                        time_entry = TimeEntry(self.start_time, end_time, 0, 0, 0, 0)
                        time_entry._get_specific_times()

                        # Activities
                        if self.output['activities']:
                            exists = False
                            for activity in self.activeList.activities: 
                                if activity.name == self.activity_name:
                                    exists = True
                                    activity.time_entries.append(time_entry)
                                    # index =self.activeList.overview.index({'name': activity.name})
                                    # print(self.activeList.overview[index])
                            if not exists:
                                activity = Activity(self.activity_name, [time_entry])
                                self.activeList.activities.append(activity)
                            

                        #OverView
                        if self.output['overview']:
                            overview_exists = False;
                            for over in self.activeList.overview:
                                if over.name == self.activity_name:
                                    overview_exists = True
                                    'Already exists an entry here'
                                    over.time_entries[0].total_time = over.time_entries[0]._total_time_ + (end_time - self.start_time)
                                    over.time_entries[0].end_time = end_time
                                    over.time_entries[0]._get_specific_times()
                            if not overview_exists:
                                activity = Activity(self.activity_name, [time_entry])
                                self.activeList.overview.append(activity)    
                        
                        # Log
                        if self.output['logs']:
                            activity_log = Activity(self.activity_name, [time_entry])  
                            self.activeList.logs.append(activity_log)

                        
                        
                        with open(f'projects/{project_name}.json', 'w') as json_file:
                            json.dump(self.activeList.serialize(), json_file, indent=4, sort_keys=True)
                            self.start_time = datetime.datetime.now()
                    first_time = False
                    self.active_window_name = new_window_name

                time.sleep(1)
    
        except KeyboardInterrupt: 
            with open(f'projects/{project_name}.json', 'w') as json_file:
                json.dump(self.activeList.serialize(), json_file, indent=4, sort_keys=True)
            for i in range(len(args_handler.runningProjects)):
                project = args_handler.runningProjects[i]
                if project['name'] == project_name:
                    del args_handler.runningProjects[i]
                    return args_handler.save_project_info()



import args_handler 
if __name__ == '__main__':
    args_handler.ArgsHandler()