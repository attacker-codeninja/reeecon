#!/usr/bin/env python3

import os
from datetime import date
from .util import *

today = date.today().strftime("%b-%d-%Y")

massdnsWordlist = home + "/wordlist/dns-Jhaddix.txt"
massdns_dir = home + "/tools/massdns/bin/massdns"
resolvers_dir = home + "/tools/massdns/lists/resolvers.txt"
subbrute_py_dir = home + "/tools/massdns/scripts/subbrute.py"


def subdomain_takeover(out_dir, target):
    os.system(
        'cat {} | {} -r {} -t A -q -o S -w {}domaintemp.txt'.format(out_dir + 'subdomain.txt', massdns_dir,
                                                                    resolvers_dir, out_dir))
    os.system(
        '{} {} {} | {} -r {} -t A -q -o S | grep -v 142.54.173.92 >> {}domaintemp.txt'.format(
            subbrute_py_dir, massdnsWordlist, target, massdns_dir, resolvers_dir, out_dir))
    test_subdomain = {}

    with open(out_dir + "domaintemp.txt", "r") as text_file, open(out_dir + 'subdomain.txt', 'a+') as subdomain:
        lines = text_file.readlines()
        for line in lines:
            record = line.split(' ')
            if record[1] == "CNAME" and record[2] not in test_subdomain.values():
                test_subdomain[record[0]] = record[2]
                subdomain.writelines(record[0] + '\n')

    with open(out_dir + "subdomain_takeover.txt", "a") as f:
        f.writelines('check the following domains for NS takeover:\n')
        for subdomain in test_subdomain.keys():
            output = os.popen("host {}".format(subdomain)).read()
            if "NXDOMAIN" in output:
                f.writelines(subdomain + '\n')

# subdomain_takeover('/root/recon_result/marriott.com/Mar-15-2020/', 'marriott.com')
