''' 
This file gives the linux support for this repo
'''
import sys
import os
import subprocess
import re


def get_active_window_raw():
    '''
    returns the details about the window not just the title
    '''
    root = subprocess.Popen(
        ['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=subprocess.PIPE)
    stdout, stderr = root.communicate()

    m = re.search(b'^_NET_ACTIVE_WINDOW.* ([\w]+)$', stdout)
    if m != None:
        window_id = m.group(1)
        window = subprocess.Popen(
            ['xprop', '-id', window_id, 'WM_NAME'], stdout=subprocess.PIPE)
        stdout, stderr = window.communicate()
    else:
        return None

    match = re.match(b"WM_NAME\(\w+\) = (?P<name>.+)$", stdout)
    if match != None:
        ret = match.group("name").strip(b'\'"\'\'')
        #print(type(ret))
        '''
        ret is str for python2
        ret is bytes for python3 (- gives error while calling in other file)
        be careful
        '''
        return ret
    return None

'''
this file alone can be run without importing other files
uncomment the below lines for linux - works - but activities won't be dumped in json file
(may be it works for other OS also, not sure)
'''
# def run():
#     new_window = None
#     current_window = get_active_window_title()
#     while(True):
#         if new_window != current_window:
#                 print(current_window)
#                 print(type(current_window))
#                 current_window = new_window
#         new_window = get_active_window_title()


# run()
def get_chrome_url_x():
        ''' 
        instead of url the name of the website and the title of the page is returned seperated by '/' 
        '''
        detail_full = str(get_active_window_raw())
        detail_list = detail_full.split(' - ')
        detail_list.pop()
        detail_list = detail_list[::-1]
        # Added By Me
        for index, word in enumerate(detail_list):
            if word[:2] in ["b'", 'b"']:
                detail_list[index] = word[2:] 
        # 
        # IT BOTHERS ME THAT THE PROGRAM CREATES A OBJECT EVERY SINGLE TIME I CHANGE OF TAB IN THE BROWSER
        # THAT'S WHY UNTIL I FIND A SOLUTION I MADE IT JUST TAKE THE WORD 'BROWSER' WHEN I'M NAVIGATING
        # _active_window_name = 'Browser -> ' + " | ".join(detail_list)
        _active_window_name = 'Browser'
        return _active_window_name



def get_active_window_x():
    '''Necesary to add str in the next line method with python 3'''
    full_detail = str(get_active_window_raw()) 
    detail_list = None if None else full_detail.split(" - ")
    # Added By Me
    for index, word in enumerate(detail_list):
        if word[:2] in ["b'", 'b"']:
            detail_list[index] = word[2:]
        if word[-1] == "'":
            detail_list[index] =  detail_list[index][:-1]
    
    new_window_name = detail_list[-1]
    return new_window_name

