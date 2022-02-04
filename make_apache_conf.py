#!/usr/bin/env python3
import yaml, re, sys, os, io
from typing import Callable


class YamlFileReader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def getYamlSafe(self):
        with open(self.file_path) as fin:
            yml = yaml.safe_load(fin)
            return yml


class TextFileLineIterator:
    def __init__(self, file_: io.TextIOWrapper):
        self.file = file_
    
    def __iter__(self):
        return self
    
    def __next__(self):
        line = self.file.readline()
        if line:
            return line
        raise StopIteration

class TextFileSubstitutor:
    """
    file_
        filestream
    tK_finder
        callable
        param: string
        returns: string
        purpose: locate a value to be substituted within string param
        
    tk_substitutor
        callable
        param: string
        returns: string
        purpose: take a string and return a value
    """
    def __init__(self, file_: io.TextIOWrapper, tk_finder: Callable, tk_mapper: Callable, tk_parser:Callable=None):
        self.file_iterator = TextFileLineIterator(file_)
        self.tk_finder = tk_finder
        self.tk_mapper = tk_mapper
        self.tk_parser = tk_parser or (lambda str_: str_[1:-1].strip())

    def _gen_next_line(self):
        for line in self.file_iterator:
            line = self.substitute_tokens(line)
            yield line

    def get_token_key(self, tk):
        return self.tk_parser(tk)

    def substitute_tokens(self, line):
        tokens = self.tk_finder(line)
        for tk in tokens:
            key = self.get_token_key(tk)
            val = self.tk_mapper(key)
            if val:
                line = line.replace(tk, val)
        return line

    def _write_to_stream(self, fout: io.TextIOWrapper):
        for line in self._gen_next_line():
            fout.write(self.substitute_tokens(line))

    def write(self, file_path: str):
        with open(file_path, 'w+') as fout:
            self._write_to_stream(fout)

def validateInput(file_name):
    return os.path.isfile(file_name)

def validateYaml(yml):
    return (type(yml) == dict) and 'GLOBAL' in yml

def getGlobalSettings(yml):
    return yml['GLOBAL']

def main(template_path: str, yml_path: str, site: str):
    yml = YamlFileReader(yml_path).getYamlSafe()

    if validateYaml(yml):
        global_settings = getGlobalSettings(yml)
        pattern = global_settings['RE_PATTERN']
        fout_key = global_settings['FOUT_KEY']
        
        params = yml[site]
        config_path = params[fout_key]

        finder = re.compile(pattern).findall
        mapper = lambda match: (match in params) and params[match]     
        with open(template_path, 'r') as fin:
            TextFileSubstitutor(fin, finder, mapper).write(config_path)
    else:
        print("Error reading yaml file")

if __name__ == '__main__':
    template_path = sys.argv[1]
    yml_path = sys.argv[2]
    site = sys.argv[3]

    if validateInput(yml_path) and validateInput(template_path):
        main(template_path, yml_path, site)
    else:
        print("Invalid file name passed")
