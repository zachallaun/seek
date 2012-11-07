# seek_functions.py #
import pdb
import os
import re
import sys
import nltk
from nltk.corpus import wordnet as wn
from sets import Set


# search
def search(args, ignore_case = 0):
    
    Found_in_lines = {}
    search_pattern = args[0]
    text_lines = read_lines_from_file(args[1])
    for line in range(len(text_lines)):
        search_result = re.search(search_pattern,text_lines[line],ignore_case)
        if search_result:
            result_line = re.sub(search_pattern, highlight, text_lines[line], flags = ignore_case)
            key, value = line, result_line
            Found_in_lines[key] = value
    return Found_in_lines, search_pattern

def search_helper(arguments, search_location, ignore_case = 0, print_filename = 0, print_line = 0):

    if search_location == os.getcwd().split():
        search_location = files_in_current_directory(search_location)
    
    if len(search_location) > 1: print_filename = 1
    for x in range (len(search_location)):
        args = arguments, search_location[x]
        results, search_terms = search(args, ignore_case)
        if search_terms.find("|"):
            search_terms = search_terms.split('|')
        else:
            search_terms = search_terms.split()   
        unique_terms = list(set(search_terms))
        filename = search_location[x]
        print_results(results, unique_terms, filename, print_filename, print_line)


# search options

def basic_search(args, ignore_case = 0):
    search_helper(args[0], args[1], ignore_case, print_line = 1)

def line_starts_with(args):
    search_arg = '^'+ args[0]
    search_helper(search_arg, args[1], print_line = 1)

def starts_with(args):
    search_arg = '\\b'+ args[0] + '\\B'
    search_helper(search_arg, args[1], print_line = 1)

def ends_with(args):
    search_arg = '\\B' + args[0] + '\\b'
    search_helper(search_arg, args[1], print_line = 1)
    
def line_ends_with(args):
    search_arg = args[0] + '$'
    search_helper(search_arg, args[1], print_line = 1)

def match_whole_word(args):
    search_arg = '\\b' + args[0] + '\\b'
    search_helper(search_arg, args[1], print_line = 1)
    
def list_filenames(args):
    search_helper(args[0],args[1], print_filename = 1)

def pattern_file(args):
    search_terms = []
    text_lines = read_lines_from_file(args[0])
    for line in text_lines:
        search_terms.append(line.strip('\n'))
    arguments = '|'.join(search_terms)
    search_helper(arguments,args[1], print_line = 1)


def recursive_dir(args):
    
    if len(args[1]) == 1:
        files = files_in_recursive_directory(args[1])
        search_helper(args[0],files, print_line = 1)
    elif len(args[1]) > 1:
        # Assumes filename wildcard to use in recursive search
        file_extension = find_file_extension(args[1])
        files = files_in_recursive_directory(os.getcwd().split(), extension = file_extension)
        search_helper(args[0],files, print_line = 1)
      

def synonym_search(args):
    search_word = args[0]
    synonyms = find_synonyms(search_word)
    print "Searching for the following synonym words: " + synonyms.replace('|',',')
    search_helper(search_word, args[1], print_line = 1)


def find_synonyms(search_word):
    syns = wn.synsets(search_word.lower())
    syns_list = []
    for s in syns:
        for l in s.lemmas:
            syns_list.append(l.name)
    return '|'.join(list(set(syns_list)))


# Common Functions

def find_file_extension(arg):
    filename, extension = os.path.splitext(arg[0])
    return extension

def files_in_recursive_directory(directory_name, extension = None):
    list_of_files = []
    for dirs, subdirs, files in os.walk(directory_name[0]):
        for i in files:
            if extension == None:
                list_of_files.append(os.path.join(dirs,i))
            else:
                if i.endswith(extension) == True: 
                    list_of_files.append(os.path.join(dirs,i))
    return list_of_files   
    
def files_in_current_directory(directory_name, extension = None):
    list_of_files = []
    for item in os.listdir(directory_name[0]):
            if extension == None:
                if os.path.isfile(os.path.join(directory_name[0], item)):
                    list_of_files.append(os.path.join(directory_name[0],item))
            else:
                pass
    return list_of_files
    

def highlight(matchobj):
    return '\033[92m' + matchobj.group(0) + '\033[0m'


def print_results(results, search_terms, filename = None, print_filename = 0, print_line = 0):
    
    for key,value in results.iteritems():
            if print_filename == 1 and print_line == 1:
                print '\n' + '\033[94m' + filename + '\033[0m' + '\033[91m' + " (Line " + str(key) + ")" + '\033[0m' + str(value).strip(' ')
            elif print_filename == 1 and print_line == 0:
                print '\n' + '\033[94m' + filename + '\033[0m' + '\033[91m' + " (Line " + str(key) + ")" + '\033[0m'
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
