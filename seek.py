####### Seek ########
# A command line tool written in Python similar to grep.
# 
# search for specific string in file
# seek <string> <filename>
#                                                            #
##############################################################
import optparse
import sys
import seek_functions
import pdb

def main(args):
    parser = optparse.OptionParser("""\nUsage: %prog [--options] [pattern] [source] [symbol] [destination]""")

   
    parser.add_option("-p","--pattern_file",
                      action="store_true",
                      dest="pattern_file",
                      default=False,
                      help="Searches for patterns from specified file.")
    parser.add_option("-i","--ignore_case",
                      action="store_true",
                      dest="ignore_case",
                      default=False,
                      help="Searches for pattern ignoring case")
    parser.add_option("-c","--word_contains",
                      action="store_true",
                      dest="word_contains",
                      default=False,
                      help="Searches for any words that include pattern")
    parser.add_option("-S","--starts_with",
                      action="store_true",
                      dest="starts_with",
                      default=False,
                      help="Searches for any words that include pattern")
    parser.add_option("-s","--line_starts_with",
                      action="store_true",
                      dest="line_starts_with",
                      default=False,
                      help="Searches for any words that include pattern")
    parser.add_option("-e","--line_ends_with",
                      action="store_true",
                      dest="line_ends_with",
                      default=False,
                      help="Searches for any words that include pattern")
    parser.add_option("-E","--ends_with",
                      action="store_true",
                      dest="ends_with",
                      default=False,
                      help="Searches for any words that include pattern")
    parser.add_option("-w","--match_whole_word",
                      action="store_true",
                      dest="match_whole_word",
                      default=False,
                      help="Searches for any words that include pattern")
    parser.add_option("-l","--list_filenames",
                      action="store_true",
                      dest="list_filenames",
                      default=False,
                      help="Searches for any words that include pattern")
    parser.add_option("-r","--recursive_dir",
                      action="store_true",
                      dest="recursive_dir",
                      default=False,
                      help="Searches for any words that include pattern")


    (opts, args) = parser.parse_args(args)
   

    if len(args) < 2:
        parser.error("wrong number of arguments")

  
    if opts.pattern_file:
        seek_functions.pattern_file(args)
    elif opts.ignore_case:
        seek_functions.basic_search(args, flag = 2)
    elif opts.word_contains:
        seek_functions.word_contains(args)
    elif opts.line_starts_with:
        seek_functions.line_starts_with(args)
    elif opts.line_ends_with:
        seek_functions.line_ends_with(args)
    elif opts.ends_with:
        seek_functions.ends_with(args)
    elif opts.match_whole_word:
        seek_functions.match_whole_word(args)
    elif opts.match_whole_word:
        seek_functions.match_whole_word(args)
    elif opts.recursive_dir:
        seek_functions.recursive_dir(args)
    elif opts.list_filenames:
        seek_functions.list_filenames(args)
    else: 
        seek_functions.basic_search(args)

if __name__ == "__main__":
    main(sys.argv[1:])
