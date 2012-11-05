# seek_functions.py #
import pdb
import os
import re
import sys
from sets import Set


# search
def search(args, flag = 0):
    
    Found_in_lines = {}
    search_pattern = args[0]
    text_lines = read_lines_from_file(args[1])
    for line in range(len(text_lines)):
        search_result = re.search(search_pattern,text_lines[line],flag)
        if search_result:
            key, value = line, text_lines[line]
            Found_in_lines[key] = value
    pdb.set_trace()
    return Found_in_lines, search_pattern


def line_starts_with(args):
    
    regex_arg = args[0]
    regex_arg = '^'+ regex_arg
    args[0] = regex_arg
    results = search(args)
    print_results(results)
    
def line_ends_with(args):
    
    regex_arg = args[0]
    regex_arg = regex_arg + '$'
    args[0] = regex_arg
    results = search(args)
    print_results(results)


def match_whole_word(args):
    
    regex_arg = args[0]
    regex_arg = '\\b' + regex_arg + '\\b'
    args[0] = regex_arg
    results = search(args)
    print_results(results)

    
#use pattern file
def pattern_file(args):
    
    pattern_file = args[0]
    search_terms = []
    #read pattern file
    text_lines = read_lines_from_file(pattern_file)
    for line in text_lines:
        search_terms.append(line.strip('\n'))
    args[0] = '|'.join(search_terms)
    results = search(args, return_lines = 1)
    print_results(results)

def recursive_dir(args):
    search_directory = args[1]
    files_in_directory(search_directory,True)


def files_in_directory(directory_name, subdir, args = None):
    pdb.set_trace()
    list_of_files = []
    listfiles = []
    for dirs, subdirs, files in os.walk(directory_name):
        for i in files:
            if args == None:
                list_of_files.append(os.path.join(dirs,i))
                #listfiles.append('\n'.join([os.path.join(dirs,i) for i in files]))
            else:
                pass
    return list_of_files

def basic_search(args, flag):
    results, search_terms = search(args, flag)
    formatted_results = highlight(results,search_terms)
    print_results(formatted_results)

def print_results(results):

    for key,value in results.iteritems():
        print "[Found in line " + str(key) + "]" + str(value)

def highlight(results, search_terms):
    results = results.replace(search_terms, '\033[92m' + search_terms + '\033[0m')
    return results


#word includes
def word_contains(args):
    pass

def read_lines_from_file(filename):

    try:
        file = open(filename,'r')
        lines = file.readlines()
        return lines
    except IOError:
        current_directory = os.getcwd()
        try:
            file = open(filename,'r')
            lines = file.readlines()
            return lines
        except:
            print("Error while opening file")
