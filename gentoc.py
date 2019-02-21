from argparse import ArgumentParser
import os
import re

CWD = os.getcwd()

#Define parameters
ARGS_HELP = {
    'filename': "Input file.",
    'output': "Name of output file.",
    'directory': "Directory of output file.\nNonleading slashes assumes relative path.\nDefaults to current working directory.",
    'write_title': "Write the first encountered H1 as the first line of the markdown. Interpretted as title in some editors. Default is true (1)."
}
parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="filename", help=ARGS_HELP['filename'], metavar="FILE")
parser.add_argument("-o", "--output", dest="output", help=ARGS_HELP['output'], default="out.md")
parser.add_argument("-d", "--dir", dest="directory", help=ARGS_HELP['directory'], default="")
parser.add_argument("-t", "--title", dest="write_title", help=ARGS_HELP['write_title'], default="1")

args = parser.parse_args()

# Interpret parameters
## Set default directory and add formatted slash to the end
if args.directory == "":
    args.directory = CWD
if args.directory[-1] != "/":
    args.directory += "/"
    
## Check leading slashes for adaptive relativity
if args.directory[0] != "/":
    pass
if not os.path.exists(args.directory):
    print("ERROR | Invalid directory: " + args.directory)
    exit()

## Manage filename validation
## Output validation
## Directory validation (-o --output)


def main():
    # table of contents list
    structure = []    
    
    in_file = open(args.filename, 'r')
    in_text = in_file.readlines()
    
    open(args.directory + args.output, 'w').close()
    out_file = open(args.directory + args.output, 'a')
    
    # handle empty files
    if len(in_text) == 0:
        print("No lines to process!")
        exit()
   
    #linenumber
    ln = 0 
    for line in in_text:
        ln += 1
        out_line = line
        
        ## Match regex # ## ### depth
        if len(line.split()) > 1:
            match = re.search("^[#]*$", line.split()[0])
            if match:
                depth = len(match[0])
                item_name = line[depth + 1:].strip('\n')
                item_id = item_name.strip('\n').lower().replace(' ', '-') #for markdown anchor names
                structure.append([ln, depth, item_name, item_id])
                
                out_line = line.strip('\n') + '<a name="' + item_id + '"></a>\n'
        
        out_file.write(out_line)
    out_file.close()

    
    ## create Table of Contents
    doc_text = open(args.directory + args.output, 'r').read()
    open(args.directory + args.output, 'w').close()
    out_file = open(args.directory + args.output, 'a')

    # Generate markdown TOC text
    if int(args.write_title) != 0:
        out_file.write("# " + structure[0][2].title() + "\n\n")
    out_file.write("## Table Of Contents \n")
    for heading in structure:
        out_file.write((heading[1] - 1) * '\t' + '- [' + heading[-2].title() + '](#' + heading[-1] + ')\n')
        
    out_file.write('\n---\n\n' + doc_text)
    out_file.close()
    
main()
