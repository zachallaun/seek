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
            result_line = re.sub(search_pattern, highlight, text_lines[line], flags = flag)
            key, value = line, result_line
            Found_in_lines[key] = value
    return Found_in_lines, search_pattern


def line_starts_with(args):
    
    regex_arg = args[0]
    regex_arg = '^'+ regex_arg
    args[0] = regex_arg
    results, search_terms = search(args)
    search_terms = search_terms.split()
    print_results(results, search_terms)
    
def line_ends_with(args):
    
    regex_arg = args[0]
    regex_arg = regex_arg + '$'
    args[0] = regex_arg
    results, search_terms = search(args)
    search_terms = search_terms.split()
    print_results(results, search_terms)


def match_whole_word(args):
    
    regex_arg = args[0]
    regex_arg = '\\b' + regex_arg + '\\b'
    args[0] = regex_arg
    results, search_terms = search(args)
    search_terms = search_terms.split()
    print_results(results, search_terms)

    
#use pattern file
def pattern_file(args):
    
    pattern_file = args[0]
    search_terms = []
    #read pattern file
    text_lines = read_lines_from_file(pattern_file)
    for line in text_lines:
        search_terms.append(line.strip('\n'))
    args[0] = '|'.join(search_terms)
    results, search_terms = search(args)
    search_terms = search_terms.split('|')
    unique_terms = list(set(search_terms))
    print_results(results, unique_terms)

def recursive_dir(args):
    search_directory = args[1]
    files = files_in_directory(search_directory,True)
    print ("Searching " + str(len(files)) + " files...")
    for x in range (len(files)):
        args[1] = files[x]
        results, search_terms = search(args)
        search_terms = search_terms.split()
        print_results(results,search_terms,filename = files[x])


def synonym_search(args):
    pass

def list_filenames(args):
    if len(args) == 1:
        search_directory = os.getcwd() 
        files = files_in_directory(search_directory,True)
        print ("Searching " + str(len(files)) + " files...")
        for x in range (len(files)):
            args = args[0],files[x]
            results, search_terms = search(args)
            search_terms = search_terms.split()
            print_results(results,search_terms,filename = files[x], flag = 1)


def files_in_directory(directory_name, subdir, args = None):
    list_of_files = []
    listfiles = []
    for dirs, subdirs, files in os.walk(directory_name):
        for i in files:
            if args == None:
                list_of_files.append(os.path.join(dirs,i))
            else:
                pass
    return list_of_files

# Performs search with no options and search with -i ignore case option using flag
def basic_search(args, flag):
    results, search_terms = search(args, flag)
    search_terms = search_terms.split()
    print_results(results, search_terms)
    

def highlight(matchobj):
    return '\033[92m' + matchobj.group(0) + '\033[0m'


def print_results(results, search_terms, filename = None, flag = 0):
    
    for key,value in results.iteritems():
            if filename:
                if flag == 1:
                    print '\n' + '\033[94m' + filename + '\033[0m' + '\033[91m' + " (Line " + str(key) + ")" + '\033[0m'
                else:
                    print '\n' + '\033[94m' + filename + '\033[0m' + '\033[91m' + " (Line " + str(key) + ")" + '\033[0,' + str(value).strip(' ')                  
            else:
                print '\n' + '\033[91m' + "(Line " + str(key) + ")" + '\033[0m' + str(value).strip(' ')
        

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
