SEEK.py
=======

Description: A grep-like command utility providing various seach options.

	Usage: Seek.py [-o | --options] [search_term] [search_location]

### EXAMPLE: 
		seek.py search_term (searches all files within current directory)
		seek.py seach_term /path/to/file (searches that file only)
		seek.py "search_term" /path/to/file (same as above)
		seek.py search_term *.extension  (searches files of .extension within current directory)

### NOTES: 

All searches within multiple files using a wild card (*) return the "file_name : line_number: text_line "

Basic search is case-sensitive.

When printing matched text lines, the search terms will be highlighted by default in green.

OPTIONS
-------

Seek.py supports the following search options:

### -p | --pattern_file :
Pull search_terms from a given file. Search terms must be separated by a newline:

		seek.py -p [path/to/search_term/file] [path/to/search_location]
		seek.py -p words.txt text_file.txt
		seek.py -p words.txt *.extension
		seek.py -p words.txt (searches all files within current directory)

### -i | --ignore_case:   
Performs case-insensitve search.
		
		seek.py -i search_term path/to/file
		seek.py -i search_term *.extension
		seek.py -i search_term (searches all files within current directory)
					  
(returns all lines matching search_term, SEARCH_TERM, SearcH_TERm etc. from path/to/file)					  		   

### -S | --starts_with:
Searches for any lines with words that start with search term.

		seek.py -S ten /path/to/file
		seek.py -S ten *.extension
		seek.py -S ten (searches all files within current directory)

(returns all lines including words such as tennis, tenure, tent, etc)

### -s | --line_starts_with:
Searches for any lines where the line starts with search term.

		seek.py -s search_term /path/to/file
		seek.py -s search_term *.extension
		seek.py -s search_term (searches all files within current directory)

### -E | --ends_with:
Searches for any lines with words that end with search term.

		seek.py -S ted /path/to/file
		seek.py -S ted *.extension
		seek.py -S ted (searches all files within current directory)

(returns all lines including words such as painted, invited, etc)

### -e | --line_ends_with:
Searches for any lines where the line ends with search term.

		seek.py -s search_term /path/to/file
		seek.py -s search_term *.extension
		seek.py -s search_term (searches all files within current directory)

### -w | --match_whole_word:
Searches for any lines with words that as a whole match the search_term.

		seek.py -w search_term /path/to/file
		seek.py -w search_term *.extension
		seek.py -w search_term (searches all files within current directory)

### -r | --recursive_dir:
Searches recursively for any lines containing search_term in files within indicated directory.

		seek.py -r search_term /path/to/directory
		seek.py -r search_term (searches current directory recursively)
		seek.py -r search_term *.extension (searches current directory recursively for files with .extension)

(returns filename: line number: line text)

### -l | --list_filenames:
Searches for any files containing search_term in current directory and returns filenames

		seek.py -l search_term (searches current directory)
		seek.py -l search_term *.extension (searches current directory for files with .extension)

### -y | --synonym_search:
Searches for any files containing a match for the search_term and *any* of the synonym words returned from the dictionary.

		seek.py -y search_term /parth/to/file
		seek.py -y search_term *.extension
		seek.py -y search_term (searches files in current directory)



