# Author: Michael Polivka
# Login: xpoliv07
# Date: 5.4.2023 - xx.xx.xxxx
# Description: Interpret for IPPcode23 - ulitilities module

import xml.etree.ElementTree as ET
from interpret_library.instruction import *
from interpret_library.error_codes import *
from interpret_library.util import Var, Label, Type, Const



class XMLParser:
    """Loads and Checks XML, then return a list of executable instructions"""
    def __init__(self, frame_stack, flow_manager, xml_file, stack):
        self.instructions_list = None
        self.__frame_stack = frame_stack
        self.__flow_manager = flow_manager
        self.stack = stack
        try:
            xml = ET.parse(xml_file)
            self.__root = xml.getroot()
        except ET.ParseError:
            error("Bad xml", ErrorCodes.xmlError)

    def parse(self):
        if self.instructions_list:
            return self.instructions_list

        else:
            self.instructions_list = []
            if self.__root.tag != "program":
                error("Root tag is not program", ErrorCodes.xmlError)
            else:
                if not re.match('^IPPcode23', self.__root.attrib['language'], re.IGNORECASE):
                    error("Bad language in XML", ErrorCodes.xmlError)

            for child in self.__root:
                if child.tag != "instruction":
                    error(f"Bad element, expected /instruction/ got {child.tag}", ErrorCodes.xmlError)
                ca = list(child.attrib.keys())
                if not ('order' in ca and 'opcode' in ca) or len(ca) != 2:
                    error("Bad attributes", ErrorCodes.xmlError)

                # Set operands for instruction
                operands = []
                for arg in child:
                    if not (re.match("arg[1-3]", arg.tag)):
                        error("Bad element, expected arg(1-3)", ErrorCodes.xmlError)
                    if 'type' not in arg.attrib and len(arg.attrib):
                        error(f"Bad attributes in arg{arg.attrib}", ErrorCodes.xmlError)
                    o_value = arg.text if arg.text else ''
                    operands.append(self.__parse_args(arg.attrib["type"], o_value))
                    #log(f"Arg: {arg.tag}, attributes: {arg.attrib}, value: {arg.text}")
                self.instructions_list.append(eval(child.attrib["opcode"])(child.attrib['opcode'],
                                                                           child.attrib['order'],
                                                                           operands,
                                                                           self.__frame_stack,
                                                                           self.__flow_manager,
                                                                           self.stack))
            self.instructions_list.append(None)

    def __parse_args(self, arg_type, value):
        if (arg_type := arg_type.lower()) == "var":
            return Var(value)
        elif arg_type == "label":
            return Label(value)
        elif arg_type == "type":
            return Type(value)
        elif arg_type in ["int", "bool", "string", "nil"]:
            return Const(arg_type, value)

    def __repr__(self):
        return self.instructions_list








