#!/usr/bin/env python
import yaml
import re

def get_yaml(file):
    y = None
    with open(file, 'r') as strm:
        y = yaml.safe_load(strm)
    return y

def get_sites(yml):
    return iter(yml.keys())

def main():
    TEMPLATE = '/var/www/apache-conf.template'
    YML_PATH = '/var/www/apache-settings.yaml'
    yml = get_yaml(YML_PATH)
    sites = get_sites(yml)
    K_SITES_AVAILABLE_PATH = 'SitesAvailableFilePath'
    PATTERN = re.compile('({\s*(.*?)\s*})')

    for site in sites:
        params = yml[site]
        with open(TEMPLATE, 'r') as fin, open('/var/www/test.conf', 'w+') as fout:
        #with open(template, 'r') as fin, open(params[K_SITES_AVAILABLE_PATH], 'w') as fout:
            while True:
                matches = None
                ln = fin.readline()
                if not ln:
                    break
                #ln = '{ServerName} { WSGIDaemonProcessName  } {GLOBAL}'
                matches = PATTERN.findall(ln)
                #print(matches)
                if matches:
                    for match in matches:
                        #print(matches, match)
                        key = match[1]
                        temp_val = match[0]
                        if key in params:
                            #print(ln)
                            ln = ln.replace(temp_val, params[key])
                            #print(ln)
                fout.write(ln)

if __name__ == '__main__':
    main()
