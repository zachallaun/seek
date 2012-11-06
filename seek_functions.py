# seek_functions.py #
import pdb
import os
import re
import sys
import nltk
from nltk.corpus import wordnet as wn
from sets import Set


# search
def search(args, ignore_case_flag = 0):
    
    Found_in_lines = {}
    search_pattern = args[0]
    text_lines = read_lines_from_file(args[1])
    for line in range(len(text_lines)):
        search_result = re.search(search_pattern,text_lines[line],ignore_case_flag)
        if search_result:
            result_line = re.sub(search_pattern, highlight, text_lines[line], flags = ignore_case_flag)
            key, value = line, result_line
            Found_in_lines[key] = value
    return Found_in_lines, search_pattern

def search_helper(arguments,search_location, ignore_case_flag = 0, print_filename_flag = 0, print_line_flag = 0):
    for x in range (len(search_location)):
        args = arguments, search_location[x]
        results, search_terms = search(args, ignore_case_flag)
        search_terms = search_terms.split()
        filename = search_location[x]
        print_results(results, search_terms, filename, print_filename_flag, print_line_flag)


# search options

def basic_search(args, ignore_case_flag = 0):
    search_helper(args[0],args[1],ignore_case_flag)

def line_starts_with(args):
    search_arg = '^'+ args[0]
    search_helper(search_arg, args[1])

def starts_with(args):
    search_arg = '\\b'+ args[0] + '\\B'
    search_helper(search_arg, args[1])

def ends_with(args):
    search_arg = '\\B' + args[0] + '\\b'
    search_helper(search_arg, args[1])
    
def line_ends_with(args):
    search_arg = args[0] + '$'
    search_helper(search_arg, args[1])

def match_whole_word(args):
    search_arg = '\\b' + args[0] + '\\b'
    search_helper(search_arg, args[1])
    
def list_filenames(args):
    if len(args[1]) == 1:
        files = files_in_directory(args[1],True)
        print ("Searching " + str(len(files)) + " files...")
        for x in range(len(files)):
            search_helper(args[0],files[x].split(), print_filename_flag = 1)
    elif len(args[1]) > 1:
        search_helper(args[0],args[1], print_filename_flag = 1)

#use pattern file
def pattern_file(args):
    pattern_file = args[0]
    search_location = args[1]
    search_terms = []
    if len(search_location) == 1:
        #read pattern file
        text_lines = read_lines_from_file(pattern_file)
        for line in text_lines:
            search_terms.append(line.strip('\n'))
        args[0] = '|'.join(search_terms)
        results, search_terms = search(args)
        search_terms = search_terms.split('|')
        unique_terms = list(set(search_terms))
        print_results(results, unique_terms)
    elif len(search_location) > 1:
        for x in range (len(search_location)):
            #read pattern file
            text_lines = read_lines_from_file(pattern_file)
            for line in text_lines:
                search_terms.append(line.strip('\n'))
            arguments = '|'.join(search_terms)
            args = arguments, search_location[x]
            results, search_terms = search(args)
            search_terms = search_terms.split('|')
            unique_terms = list(set(search_terms))
            print_results(results, unique_terms, filename = search_location[x])


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
    search_location = args[1]
    search_word = args[0]
    synonyms = find_synonyms(search_word)
    print "Searching for the following synonym words: " + synonyms.replace('|',',')
    if len(search_location) == 1:
        args = synonyms, search_location
        results, search_terms = search(args)
        search_terms = search_terms.split('|')
        unique_terms = list(set(search_terms))
        print_results(results, unique_terms)
    elif len(search_location) > 1:
        for x in range (len(search_location)):
            args = synonyms, search_location[x]
            results, search_terms = search(args)
            search_terms = search_terms.split('|')
            unique_terms = list(set(search_terms))
            print_results(results, unique_terms, filename = search_location[x])

def find_synonyms(search_word):
    syns = wn.synsets(search_word.lower())
    syns_list = []
    for s in syns:
        for l in s.lemmas:
            syns_list.append(l.name)
    return '|'.join(list(set(syns_list)))





#Helper Functions

def files_in_directory(directory_name, subdir, args = None):
    list_of_files = []
    listfiles = []
    for dirs, subdirs, files in os.walk(directory_name[0]):
        for i in files:
            if args == None:
                list_of_files.append(os.path.join(dirs,i))
            else:
                pass
    return list_of_files   
    

def highlight(matchobj):
    return '\033[92m' + matchobj.group(0) + '\033[0m'


def print_results(results, search_terms, filename = None, print_filename_flag = 0, print_line_flag = 0):
    
    for key,value in results.iteritems():
            if print_filename_flag == 1 and print_line_flag == 1:
                print '\n' + '\033[94m' + filename + '\033[0m' + '\033[91m' + " (Line " + str(key) + ")" + '\033[0m' + str(value).strip(' ')
            elif print_filename_flag == 1 and print_line_flag == 0:
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
