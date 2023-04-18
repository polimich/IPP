# Author: Michael Polivka
# Login: xpoliv07
# Date: 5.4.2023 - xx.xx.xxxx
# Description: Interpret for IPPcode23 - core module


import argparse
from interpret_library.XML_parser import *
import os


class Interpret:
    def __init__(self):
        self.__frame_stack = Frame()
        self.__instructionList = []
        self.__stack = []
        self.__flow_manager = FlowManager()

        # Parse arguments
        self.__parse_args()

    def __parse_args(self):
        # Check arguments
        ap = argparse.ArgumentParser()
        ap.add_argument("--source", required=False, type=argparse.FileType('r'), help="Source file with XML code")
        ap.add_argument("--input", required=False, type=argparse.FileType('r'), help="Input file with actual input")
        self.args = vars(ap.parse_args())
        #print(self.args['source'])

        if self.args["source"] and self.args["input"]:
            if not os.path.isfile(self.args["source"].name):
                error("Source file error", ErrorCodes.inFileError)
            if not os.path.isfile(self.args["input"].name):
                error("Input file error", ErrorCodes.inFileError)
        else:
            if self.args["source"] is None and self.args["input"]:
                self.args["source"] = 'sys.stdin'
                try:
                    sys.stdin = open(self.args["input"], 'r')
                except IOError:
                    error("Error opening input file", ErrorCodes.inFileError)

            elif self.args["input"] is None and self.args["source"]:
                self.args["input"] = 'sys.stdin'
            else:
                error("File error", ErrorCodes.inFileError)

    def run(self):
        self.__parse_args()
        xml = XMLParser(self.__frame_stack,
                        self.__flow_manager,
                        self.args["source"] if self.args["source"] != 'sys.stdin' else sys.stdin,
                        self.__stack)
        xml.parse()
        self.__instructionList = xml.instructions_list
        self.get_labels()
        self.exec()

    def get_labels(self):

        for inst in self.__instructionList:
            if isinstance(inst, LABEL):
                inst.exec()
                self.__instructionList[self.__flow_manager.instruction_counter] = NOP(inst.args[0].value,
                                                                                      inst.order,
                                                                                      [],
                                                                                      self.__frame_stack,
                                                                                      self.__flow_manager,
                                                                                      self.__stack)
            self.__flow_manager.instruction_counter += 1
        self.__flow_manager.instruction_counter = 0

    def exec(self):
        while True:
            instruction = self.__instructionList[self.__flow_manager.instruction_counter]
            if instruction is None:
                break

            instruction.exec()
            self.__flow_manager.instruction_counter += 1

