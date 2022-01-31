"""
Date ......: 30/01/2022
Developer .: Jaskaran Narula <narula.jaskaran@gmail.com>|<janarula@redhat.com>
Purpose ...: Add the # of content hosts affected by the errata
License ...: GPL3


DISCLAMER: THIS IS NOT A RED HAT SHIPPED SCRIPT. THIS IS A CUSTOM MADE SCRIPT.
"""


import csv
import requests
import json
import getopt, sys
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

argumentList = sys.argv[1:]
options = "u:p:s:e:"


long_options = ["user=", "password=", "satellite=", "erratum_id="]

try:
    arguments, values = getopt.getopt(argumentList, options, long_options)
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-u", "--user"):
            USER = currentValue
        elif currentArgument in ("-p", "--password"):
            PASSWORD = currentValue
        elif currentArgument in ("-s", "--satellite"):
            SATELLITE_FQDN = currentValue
        elif currentArgument in ("-e", "--erratum_id"):
            ERRATUM_ID = currentValue
except getopt.error as err:
    print (str(err))

Params = {
          "errata_restrict_applicable": True,
          "errata_restrict_installable": True,
          "per_page": 10000,
          "page": 1,
         }

def get_kernel_version(id):
    URL = "https://" + SATELLITE_FQDN + '/api/hosts/' + id + '/packages'
    Params = {
              "per_page": 10000,
              "page": 1,
              "search": {
                "kernel"
                }
             }
    response = requests.get(URL, Params, auth=HTTPBasicAuth(USER, PASSWORD), verify=False)
    data = json.loads(response.content)
    try:
        version = data['results'][0]['nvrea']
    except:
        version = ''
    return version


def get_errata_info(id):
    URL = "https://" + SATELLITE_FQDN + '/api/hosts/' + id + '/errata/'
    Params = {
              "per_page": 10000,
              "page": 1,
            }
    response = requests.get(URL, Params, auth=HTTPBasicAuth(USER, PASSWORD), verify=False)
    data = json.loads(response.content)
    try:
        for i in data['results']:
            errata_id   = i['errata_id'] #Fail when errata are empty
            cves = ''
            if errata_id == ERRATUM_ID:
                for j in i['cves']:
                    x = j['cve_id'] + ","
                    cves += x
                return (errata_id,cves)

    except:
        return (none, none)




# drivercode
def main():
    """
    Funtion to make the API resquest as per the API metioned in URL variable below.
    APIs can be:
    1) /api/hosts/ (default)
    """

    print("~~~~~"*20)
    print("\t DISCLAMER: THIS IS NOT A RED HAT SHIPPED SCRIPT. THIS IS A CUSTOM MADE SCRIPT")
    print("~~~~~"*20)


    URL = "https://" + SATELLITE_FQDN + '/api/hosts/'
    response = requests.get(URL, Params, auth=HTTPBasicAuth(USER, PASSWORD), verify=False)
    data = json.loads(response.content)

    total_hosts = [['Host ID','Host IP','Server Hostname','Operating System','Current Kernel Installed','Errata Released Date','Applied CVE']]

    for i in data['results']:
        id      = i['id']
        ip      = i['ip']
        name    = i['name']
        os_name = i['operatingsystem_name']
        kernel                                      = get_kernel_version(str(id))
        try:
            Errata_Released_Date, Applied_CVE_Number    = get_errata_info(str(id))
            total_hosts.append( [id, ip, name, os_name, kernel, Errata_Released_Date, Applied_CVE_Number] )
        except:
            pass

    print("\n")

    with open("/tmp/results.csv", "w") as csv_file:
        writer = csv.writer(csv_file)
        for lines in total_hosts:
            writer.writerow(lines)

    print("Task completed. Please, check the file '/tmp/results.csv'")


if __name__ == "__main__":
    main()
