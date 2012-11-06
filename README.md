SEEK.py
=======

Description: A grep-like command utility providing various seach options.

	Usage: Seek.py [-o | --options] [search_term] [search_location]

### EXAMPLE: 
		seek.py seach_term /path/to/file (searches that file only)
		seek.py "search_term" /path/to/file (same as above)
		seek.py search_term *.extension  (searches within current directory)

### NOTE: 

All searches within multiple files using a wild card (*) return the "file_name : text_line" unless -n option is used. In which case, results will also include line number as: "file_name: line_number: text_line"

Basic search is case-sensitive.


OPTIONS
-------

Seek.py supports the following search options:

### -p | --pattern_file :
Pull search_terms from a file. Search terms must be separated by a newline

EXAMPLE: 
	seek.py -p path/to/search/file path/to/file
	seek.py -p words.txt text_file.txt
	seek,py -p words.txt *.extension

-i | --ignore_case:   Performs case-insensitve search.
					  EXAMPLE: seek.py -i search_term path/to/file
					  		   seek.py -i search_term *.extension
					  
					  (returns all lines matching search_term, SEARCH_TERM, SearcH_TERm etc. from path/to/file)					  		   

-S | --starts_with:   Searches for any lines with words that start with search term.
					  EXAMPLE: seek.py -S ten /path/to/file
					  		   seek.py -S ten *.extension

					  (returns all lines including words such as tennis, tenure, tent, etc)

-s | --line_starts_with: Searches for any lines where the line starts with search term.
						 EXAMPLE: seek.py -s search_term /path/to/file
						 		  seek.py -s search_term *.extension

-E | --ends_with:   Searches for any lines with words that end with search term.
					EXAMPLE: seek.py -S ted /path/to/file
					  		 seek.py -S ted *.extension

					  (returns all lines including words such as painted, invited, etc)

-e | --line_ends_with: Searches for any lines where the line ends with search term.
					   EXAMPLE: seek.py -s search_term /path/to/file
						 		seek.py -s search_term *.extension

-w | --match_whole_word: Searches for any lines with words that as a whole match the search_term.
						 EXAMPLE: seek.py -w search_term /path/to/file
						 		  seek.py -w search_term *.extension

-r | --recursive_dir:  Searches recursively for any lines containing search_term in files within 						indicated directory.
					   EXAMPLE: seek.py -r search_term /path/to/directory
					            seek.py -r search_term *.extension (searches current directory recursively for files with .extension)
					    (returns filename: line number: line text)

-l | --list_filenames: Searches for any files containing search_term in current directory and
					   returns filenames
					   EXAMPLE: seek.py -l search_term
					            seek.py -l search_term *.extension

-y | --synonym_search: Searches for any files containing a match for the search_term and *any* of 
					   the synonym words returned from the dictionary API.
					   EXAMPLE: seek.py -y search_term /parth/to/file
					            seek.py -y search_term *.extension



