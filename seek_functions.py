# seek_functions.py #
import os
import re
import sys

# search
def search((pattern, location), ignore_case=False):
    regex_flags = 0
    if ignore_case:
        regex_flags += re.IGNORECASE
    Found_in_lines = {}
    text_lines = read_lines_from_file(location)
    for line_no, line in enumerate(text_lines):
        if re.search(pattern, line, regex_flags):
            result_line = re.sub(pattern, highlight, line, flags=regex_flags)
            Found_in_lines[line_no] = result_line
    return Found_in_lines, pattern

def search_helper(arguments, location, ignore_case=False, print_filename=0, print_line=0):
    if location == [os.getcwd()]:
        # Right now, we only support a single location
        location = files_in_directory(location[0])

    if len(location) > 1:
        print_filename = 1

    for x in range(len(location)):
        results, search_terms = search((arguments, location[x]), ignore_case)
        # Would we ever want to split on whitespace?
        if search_terms.find("|"):
            search_terms = search_terms.split('|')
        else:
            search_terms = search_terms.split()
        unique_terms = list(set(search_terms))
        filename = location[x]
        print_results(results, unique_terms, filename, print_filename, print_line)


# search options
def searchfn(fn, print_line=1, print_filename=0):
    def searcher((pattern, location), ignore_case=False):
        search_helper(fn(pattern), location, ignore_case=ignore_case,
                        print_line=print_line, print_filename=print_filename)
    return searcher

basic_search        = searchfn(lambda p: p)
line_starts_with    = searchfn(lambda p: '^' + p)
starts_with         = searchfn(lambda p: r'\b' + p + r'\B')
ends_with           = searchfn(lambda p: r'\B' + pattern + r'\b')
line_ends_with      = searchfn(lambda p: p + '$')
match_whole_word    = searchfn(lambda p: r'\b' + p + r'\b')
list_filenames      = searchfn(lambda p: p, print_line=0, print_filename=1)


def pattern_file((pattern, location)):
    arguments = '|'.join(line.strip('\n') for line in read_lines_from(pattern))
    search_helper(arguments, location, print_line=1)


def recursive_dir((pattern, location)):
    if len(location) == 1:
        search_dir = location[0]
        extension = None
    else:
        search_dir = os.getcwd()
        extension = find_file_extension(location)

    files = files_in_directory(search_dir, extension=extension, recursive=True)
    search_helper(pattern, files, print_line=1)


def synonym_search((pattern, location)):
    synonyms = find_synonyms(pattern)
    print "Searching for the following synonym words: " + synonyms.replace('|', ',')
    search_helper(pattern, location, print_line=1)


def find_synonyms(search_word):
    return ""
    #syns = wordnet.synsets(search_word.lower())
    #syns_list = []
    #for s in syns:
    #    for l in s.lemmas:
    #        syns_list.append(l.name)
    #return '|'.join(list(set(syns_list)))


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
        with open(filename, "r") as file:
            return file.readlines()
    except IOError as e:
        print "\033[91mError while opening file\033[0m"
        raise e
