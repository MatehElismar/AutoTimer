
import datetime
import json
import settings
from dateutil import parser


class AcitivyList:

    def __init__(self, activities, logs, overview):
        self.activities = activities
        self.overview = overview 
        self.logs = logs 
        

    def initialize_me(self, project_name):
        activity_list = AcitivyList([], [], [])
        with open('projects/'+project_name+'.json', 'r') as f:
            data = json.load(f)
            activity_list = AcitivyList(
                activities = self.get_property_from_json(data, 'activities'),
                overview = self.get_property_from_json(data, 'overview'),
                logs = self.get_property_from_json(data, 'logs'),
            )
        return activity_list
            


    # Changed By Me
    def get_property_from_json(self, data, field):
        return_list = [] 
        try:
            for activity in data[field]:
                return_list.append(
                    Activity(
                        name = activity['name'],
                        time_entries = self.get_time_entires_from_json(activity),
                    )
                ) 
            return return_list 
        except Exception:
            print(f'No field {field} found')
            return []

    def get_time_entires_from_json(self, data):
        return_list = []
        for entry in data['time_entries']:
            return_list.append(
                TimeEntry(
                    start_time = parser.parse(entry['start_time']),
                    end_time = parser.parse(entry['end_time']),
                    days = entry['days'],
                    hours = entry['hours'],
                    minutes = entry['minutes'],
                    seconds = entry['seconds'],
                )
            )
        self.time_entries = return_list
        return return_list
    
    def serialize(self):
        return {
            'activities' : self.activities_to_json(),
            'overview'   : self.overview_to_json(),
            'logs'       : self.logs_to_json() 
        }
    
    def activities_to_json(self):
        activities_ = []
        for activity in self.activities:
            activities_.append(activity.serialize())
        
        return activities_

    # Added By Me
    def logs_to_json(self):
        logs_ = []
        for log in self.logs:   
            logs_.append(log.serialize())
        
        return logs_
    
    # Added By Me
    def overview_to_json(self):
        overview_ = []
        for single_overview in self.overview:
            overview_.append(single_overview.serialize())
        return overview_


class Activity:
    def __init__(self, name, time_entries):
        self.name = name
        self.time_entries = time_entries

    def serialize(self):
        return {
            'name' : self.name,
            'time_entries' : self.make_time_entires_to_json()
        }
    
    def make_time_entires_to_json(self):
        time_list = []
        for time in self.time_entries:
            time_list.append(time.serialize())
        return time_list


class TimeEntry:
    def __init__(self, start_time, end_time, days, hours, minutes, seconds):
        self.start_time = start_time
        self.end_time = end_time
        self.total_time = end_time - start_time
        self.days = days
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
    

    @property
    def _total_time_(self):
        return datetime.timedelta(
            days=self.days,
            hours=self.hours,
            minutes=self.minutes, 
            seconds=self.seconds
        )

    def _get_specific_times(self):
        self.days, self.seconds = self.total_time.days, self.total_time.seconds
        self.hours = self.days * 24 + self.seconds // 3600
        self.minutes = (self.seconds % 3600) // 60
        self.seconds = self.seconds % 60

    def serialize(self):
        return {
            'start_time' : self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'end_time' : self.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            'days' : self.days,
            'hours' : self.hours,
            'minutes' : self.minutes,
            'seconds' : self.seconds
        }