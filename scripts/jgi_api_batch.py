#!/usr/bin/env python

"""
jgi_api_batch.py: batch download with JGI API

Usage:
  jgi_api_batch.py [options] <username> <password> <genome_portal>...
  jgi_api_batch.py -h | --help
  jgi_api_batch.py --version

Options:
  <username>       User name
  <password>       Password
  <genome_portal>  genome portal ID.
  -a=<a>           Path to anaconda executable.
  -f=<f>...        Folders to select from (comma-separated list).
                   [default: Raw Data,QC and Genome Assembly,IMG Data,QC Filtered Raw Data]
  -b=<b>           Base directory for output. [default: .]
  -l               List data as a table and exit.
  --version        Show version.
  -h --help        Show this screen.

Description:
  Batch download of files using the JGI-IMG API (http://genome.jgi.doe.gov/help/download.jsf).
  You will need >=1 genome portal ID (see the JGI-IMG API website). 
  You can list the possible files to download with `-l`. 
"""

from docopt import docopt
import sys
import os
import re
import subprocess
import tempfile
import xml.etree.ElementTree as etree
from pprint import pprint


def curl_bash(gp, args):
    """
    #Args
    * gp = genome portal ID
    * args = usr args
    """
    # path export
    cmd_ex = None
    if args['-a']:
        cmd_ex = 'export PATH={}:$PATH'.format(args['-a'])

    # curl
    url = 'https://signon.jgi.doe.gov/signon/create'
    curl_cmd1 = "curl '{}' --data-urlencode 'login={}' --data-urlencode 'password={}' -c cookies"
    curl_cmd1 = curl_cmd1.format(url, args['<username>'], args['<password>'])
    curl_cmd2 = "curl 'http://genome.jgi.doe.gov/ext-api/downloads/get-directory?organism={}' -b cookies"
    curl_cmd2 = curl_cmd2.format(gp)

    # writing file
    tmp_dir = tempfile.mkdtemp()
    tmp_file = os.path.join(tmp_dir, 'curl_job.sh')
    with open(tmp_file, 'w') as outFH:
        outFH.write('#!/bin/bash' + '\n')
        outFH.write(cmd_ex + '\n')
        outFH.write(curl_cmd1 + '\n')
        outFH.write(curl_cmd2 + '\n')
    return tmp_file

def call_bash(gp, bash_file):
    # call bash script
    xml_str = subprocess.check_output(['bash', bash_file])
    xml_str = xml_str.decode('utf-8')
    # remove html
    xml_str = re.sub('<html>.+html>', '', xml_str)
    # status
    print('#portal={}; xml_length={}'.format(gp, len(xml_str)), file=sys.stderr)
    return xml_str


def root_list(gp, root):
    for child in root:
        try:
            name1 = child.attrib['name']
        except KeyError:
            name1 = ''
        for gchild in child:
            for k,v in gchild.attrib.items():            
                print('\t'.join([gp, name1, k, v]))
    

def get_urls(root, args):
    urls = {}
    for child in root:
        try: 
            name_id = child.attrib['name']
        except KeyError:
            continue        
        if name_id in args['-f']:
            for gchild in child:
                try:
                    url = gchild.attrib['url']
                    filename = gchild.attrib['filename']
                    urls[filename] = url
                except KeyError:
                    pass
    return urls


def dl(gp, root, args):
    # output directory
    out_dir = os.path.join(args['-b'], gp)
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    # download with curl
    base_url = 'http://genome.jgi.doe.gov'
    cmd = 'curl "{}{}" -b cookies > {}'
    for child in root:
        try: 
            name_id = child.attrib['name']
        except KeyError:
            continue        
        if name_id in args['-f']:
            name_id = name_id.replace(' ', '_')
            # making directory
            out_dir_sub = os.path.join(out_dir, name_id)
            if not os.path.isdir(out_dir_sub):
                os.makedirs(out_dir_sub)

            # writing files
            for gchild in child:
                try:
                    url = gchild.attrib['url']            
                    filename = gchild.attrib['filename']  
                except KeyError:
                    continue
                curl_call(out_dir_sub, url, filename)



def curl_call(out_dir, url, filename):
    out_file = os.path.join(out_dir, filename)
    base_url = 'http://genome.jgi.doe.gov'
    cmd = 'curl "{}{}" -b cookies > {}'                        
    cmd1 = cmd.format(base_url, url, out_file)
    print(cmd1)
    subprocess.call(cmd1, shell=True)



def main(args):
    for gp in args['<genome_portal>']:
        bash_file = curl_bash(gp, args)
        xml_str = call_bash(gp, bash_file)
        root = etree.fromstring(xml_str)
        if args['-l']:
            root_list(gp, root)
        else:
            dl(gp, root, args)


if __name__ == '__main__':
    args = docopt(__doc__, version='0.1')
    try:
        args['-f'] = set(args['-f'].split(','))
    except KeyError:
        pass
    main(args)
