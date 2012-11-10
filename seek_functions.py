# seek_functions.py #
import os
import re
import sys


# search
def search(args, ignore_case=False):
    regex_flags = 0
    if ignore_case:
        regex_flags += re.IGNORECASE
    Found_in_lines = {}
    search_pattern = args[0]
    text_lines = read_lines_from_file(args[1])
    for line in range(len(text_lines)):
        search_result = re.search(search_pattern, text_lines[line], regex_flags)
        if search_result:
            result_line = re.sub(search_pattern, highlight, text_lines[line], flags=regex_flags)
            key, value = line, result_line
            Found_in_lines[key] = value
    return Found_in_lines, search_pattern

def search_helper(arguments, search_location, ignore_case=False, print_filename=0, print_line=0):
    if search_location == [os.getcwd()]:
        # Right now, we only support a single location
        search_location = files_in_directory(search_location[0])

    if len(search_location) > 1:
        print_filename = 1
    for x in range(len(search_location)):
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

def basic_search((pattern, location), ignore_case=False):
    search_helper(pattern, location, ignore_case, print_line=1)

def line_starts_with((pattern, location)):
    search_arg = '^' + pattern
    search_helper(search_arg, location, print_line=1)

def starts_with((pattern, location)):
    search_arg = '\\b' + pattern + '\\B'
    search_helper(search_arg, location, print_line=1)

def ends_with((pattern, location)):
    search_arg = '\\B' + pattern + '\\b'
    search_helper(search_arg, location, print_line=1)

def line_ends_with((pattern, location)):
    search_arg = pattern + '$'
    search_helper(search_arg, location, print_line=1)

def match_whole_word((pattern, location)):
    search_arg = '\\b' + pattern + '\\b'
    search_helper(search_arg, location, print_line=1)

def list_filenames((pattern, location)):
    search_helper(pattern, location, print_filename=1)

def pattern_file((pattern, location)):
    search_terms = []
    text_lines = read_lines_from_file(pattern)
    for line in text_lines:
        search_terms.append(line.strip('\n'))
    arguments = '|'.join(search_terms)
    search_helper(arguments, location, print_line=1)


def recursive_dir((pattern, location)):
    if len(location) == 1:
        files = files_in_directory(location[0], recursive=True)
        search_helper(pattern, files, print_line=1)
    elif len(location) > 1:
        # Assumes filename wildcard to use in recursive search
        file_extension = find_file_extension(location)
        files = files_in_directory(os.getcwd(), extension=file_extension,
                                   recursive=True)
        search_helper(pattern, files, print_line=1)


def synonym_search((pattern, location)):
    synonyms = find_synonyms(pattern)
    print "Searching for the following synonym words: " + synonyms.replace('|', ',')
    search_helper(pattern, location, print_line=1)


def find_synonyms(search_word):
    syns = wn.synsets(search_word.lower())
    syns_list = []
    for s in syns:
        for l in s.lemmas:
            syns_list.append(l.name)
    return '|'.join(list(set(syns_list)))


# Common Functions

def find_file_extension(filenames):
    filename, extension = os.path.splitext(filenames[0])
    return extension


def files_in_directory(dir_name, extension=None, recursive=False):
    if recursive:
        files = (os.path.join(directory, f) for directory, _, files in os.walk(dir_name) for f in files)
    else:
        files = os.listdir(dir_name)

    return [f for f in files if not extension or f.endswith(extension)]


def highlight(matchobj):
    return '\033[92m' + matchobj.group(0) + '\033[0m'


def format_line_no(no):
    return "\033[91m (Line {}) \033[0m".format(no)


def format_filename(filename):
    return "\033[94m{}\033[0m".format(filename)


def format_line(line):
    return str(line).strip(" ")


def print_results(results, search_terms, filename, print_filename=False, print_line=False):
    for line_no, line in results.iteritems():
        output = '\n'
        output += format_filename(filename) if print_filename else ""
        output += format_line_no(line_no) if print_line else ""
        output += format_line(line)
        print output


def read_lines_from_file(filename):
    try:
        file = open(filename, 'r')
        lines = file.readlines()
        return lines
    except IOError:
        current_directory = os.getcwd()
        try:
            file = open(filename, 'r')
            lines = file.readlines()
            return lines
        except:
            print("Error while opening file")
