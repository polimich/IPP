# Author: Michael Polivka
# Login: xpoliv07
# Date: 5.4.2023 - xx.xx.xxxx
# Description: Interpret for IPPcode23 - core module


import re
import argparse
import xml.etree.ElementTree as ET 

import util
import error_codes


err = error_codes.ErrorCodes()
instructions = []
# Check arguments 
ap = argparse.ArgumentParser()
ap.add_argument("--source", required=False, type=argparse.FileType('r'), help="Source file with XML code")
ap.add_argument("--input", required=False, type=argparse.FileType('r'), help="Input file with actual input")
args = vars(ap.parse_args())

if not (args["source"] and args["input"]):
    print("Error: Missing arguments")
    exit(err.badParameter)

#TODO: Check if whether source or input is missing, if so, use stdin/stdout

tree = ET.parse(args["source"])
root = tree.getroot()

if root.tag != "program":
    print("Error: Root tag is not program")
    exit(err.xmlError)
for child in root:
    if child.tag != "instruction":
        print("Error: Root tag is not program")
        exit(err.xmlError)
    ca = list(child.attrib.keys())
    if not ('order' in ca and 'opcode' in ca):
        print("Error: Missing order or opcode attribute")
        exit(err.xmlError)
    for subchild in child:
        if not(re.match ("arg[1-3]", subchild.tag)):
            print("Error: Unknown tag")
            exit(err.xmlError)
    

# instructions in root by order 
print(root[0].attrib["order"])
for e in root:
    inst = util.Instruction(e.attrib["opcode"], e.attrib["order"])
    for sub in e:
        inst.add_arg(util.Arg(sub.attrib["type"], sub.text))
    instructions.append(inst)
print(instructions)
print("success")