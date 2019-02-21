# generateTOC

*Automatically generate a clean Table of Contents for your markdown files, with universal links to respective sections.*

This project was created to extend the functionality of simple markdown editors (specifically [Joplin](https://github.com/laurent22/joplin/)) which don't natively support the "[TOC]" shorthand.

I plan to contribute to Joplin once I polish and refine the code.

## Parameters

| <span style="font-size:80%">Parameter</span> | <span style="font-size:80%">Flags</span> | <span style="font-size:80%">Desc.</span> | <span style="font-size:80%">Default</span> |
| -------------------------------------------- | ---------------------------------------- | ---------------------------------------- | ------------------------------------------ |
| filename                                     | -f --file                                | path to file                             | none                                       |
| output                                       | -o --output                              | output filename                          | out.md                                     |
| directory                                    | -d --dir                                 | output directory                         | ./                                         |

## Examples

- Overwrite your existing file by setting the output to the input file.

  ```
  python gentoc.py -f myfile.md -o myfile.md
  ```

- Generate a  TOC for each file in a directory

  ```bash
  ls | grep .md | while read -r line; do
  	python gentoc.py -f $line -o $line
  done
  	
  ```
### Todo

- Implement filesystem validation
- Strengthen illegal character handling
- Give more CLI feedback
  

