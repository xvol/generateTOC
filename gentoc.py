from argparse import ArgumentParser
import os
import re
import string
import random

CWD = os.getcwd()

#Define parameters
ARGS_HELP = {
    'filename': "Input file.",
    'output': "Name of output file.",
    'directory': "Directory of output file.\nNonleading slashes assumes relative path.\nDefaults to current working directory.",
    'write_title': "Flag: Write the first encountered H1 as the first line of the markdown. Interpretted as title in some editors.",
    'clipboard': "Flag: Take the contents of the clipboard and replace it with the TOC formatted text.\."
}

parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="filename", help=ARGS_HELP['filename'], metavar="FILE")
parser.add_argument("-o", "--output", dest="output", help=ARGS_HELP['output'], default="out.md")
parser.add_argument("-d", "--dir", dest="directory", help=ARGS_HELP['directory'], default="")
parser.add_argument("-t", "--title", dest="write_title", help=ARGS_HELP['write_title'], default="0", action='store_true')
parser.add_argument("-c", "--clipboard", dest="clipboard", help=ARGS_HELP['clipboard'], default="0", action='store_true')
args = parser.parse_args()

# Interpret parameters
if args.clipboard:
    import pyperclip
else:
    ## Manage filename validation
    ## Output validation
    ## Directory validation (-o --output)
    
    ## Check leading slashes for adaptive relativity
    if args.directory[0] != "/":
        pass
    if not os.path.exists(args.directory):
        print("ERROR | Invalid directory: " + args.directory)
        exit()
    
    ## Set default directory and add formatted slash to the end
    if args.directory == "":
        args.directory = CWD
    if args.directory[-1] != "/":
        args.directory += "/"
    


def main():
    def random_word(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))
    
    def gentoc(IN_TEXT):
        structure = []
        
        # handle empty files
        if len(IN_TEXT) == 0:
            print("ERROR: No lines to process!")
            return None
        
        lines = IN_TEXT.split('\n')
        output = ""
        toc = ""
        title = ""
        #linenumber
        ln = 0
        depth = 1
        # Generate anchors; write to output
        for line in lines:
            ln += 1
            out_line = line + '\n'

            ## Match regex # ## ### depth
            if len(line.split()) > 1:
                # Generate anchors
                match = re.search("^[#]*$", line.split()[0])
                if match:
                    depth = len(match[0])
                    
                    # skip title anchor when user specifies
                    if int(args.write_title) and depth == 1:
                        title = line.strip()[depth + 1:].strip('\n')
                        continue
                        
                    item_name = line.strip()[depth + 1:].strip('\n')
                    # randomize anchor names to avoid conflicts of headers with same name
                    item_id = item_name.strip('\n').lower().replace(' ', '-') + "-" + random_word(6)
                    
                    structure.append([ln, depth, item_name, item_id])
                    out_line = line.strip('\n') + '<a name="' + item_id + '"></a>\n'
                    
            output += out_line
        
        # Generate table of contents
        if int(args.write_title):
            toc += "# " + title.title() + "\n<hr/>\n"
        toc += "## Table Of Contents \n"
        for heading in structure:
            # essentially: add the following number of indents:
            # (number of hashes) - 1 - (condition: --title == 1?)
            # When --title == 0, indents include title as TOC
            toc += (heading[1] - (1 + int(args.write_title))) * '\t'
            toc += '- [' + heading[2].title() + '](#' + heading[-1] + ')\n'
        
        toc += '\n---\n\n'
        output = toc + output
        
        return output
    
    
    # Send output to file / clipboard
    if (int)(args.clipboard) == 1:
        in_file = pyperclip.paste()
        pyperclip.copy(gentoc(in_file))
    else:
        in_file = open(args.filename, 'r').read()
        out_file = args.directory + args.output
        open(out_file, 'w').close()
        open(out_file, 'w').write(gentoc(in_file))
    
main()
