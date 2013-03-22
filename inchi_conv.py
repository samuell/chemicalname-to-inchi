# -*- coding: utf-8 -*-
'''
Created on Fri Mar 22 12:42:19 2013

@author: Samuel Lampa - samuel.lampa@gmail.com
'''

import requests
import xmltodict
import optparse
import sys

def main():
    # Get the query compound name from the command line parameters
    opts = parse_commandline_opts()
    query_compound_name = opts.query_string
    
    # Base URL of the Chemical Translation Service
    base_url = "http://uranus.fiehnlab.ucdavis.edu:8080/cts/transform/transform"
    
    # Create a dictionary with the query parameters
    query_params = { "format" : "xml",
                       "extension" : "xml",
                       "to" : "inchikey",
                       "idValue" : query_compound_name,
                       "from" : "name"}
                             
    # Execute the query
    response = requests.get(base_url, params=query_params)
    
    # Parse the XML into a python dict (array) structure
    xmldict = xmltodict.parse(response.text)
    
    # Extract the Inchi key from the array structure
    chem_data = xmldict['compoundResultSets']['compoundResultSet']
    inchi_key = chem_data['inchiHashKey']
    
    print "Inchi key: %s" % inchi_key

def parse_commandline_opts():
    op = optparse.OptionParser()
    op.add_option("-q", "--query-string", 
                  help="Query string. Should be a chemical name" + 
                       "such as 'phenobarbital'")
    opts,args = op.parse_args()
    if not opts.query_string:
        sys.exit("You have to specify chemical name and output format!" + 
                 "Use -h flag to view options")
    return opts

# Execute main funtion if this file is the starting point
if __name__ == '__main__':
    main()
