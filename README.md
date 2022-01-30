# Host Errata Info


The main idea of this script is to generate a csv errata report as in Satellite webUI, including the # of affected content hosts.

## How to use this script. 

1. Download the python scripts to any desired directory/System or on your Red Hat Satellite 6.10. 

Note: The desired system should have python3. 

2. Run the scripts as below.

#### Usage
~~~
# wget https://github.com/JaskaranNarula/Host_Errata_Info/blob/main/Host_Errata_info.py

# python3 Host_Errata_info.py --user admin --password changme --satellite satellite.example.com -e RHSA-20XX-XXXX
~~~

# Examples
~~~
```
# cat /tmp/results.csv
Host ID,Host IP,Server Hostname,Operating System,Current Kernel Installed,Errata Released Date,Applied CVE
3,xx.xx.xxx.xxx,host1.example.com,RedHat 7.7,kernel-3.10.0-1062.18.1.el7.x86_64,RHSA-2022:0063,"CVE-2020-25704,CVE-2020-36322,CVE-2021-42739,"
2,xxx.xx.xx.xxx,host2.example.com,RedHat 7.9,kernel-3.10.0-1160.el7.x86_64,RHSA-2022:0063,"CVE-2020-25704,CVE-2020-36322,CVE-2021-42739,"
...
```
~~~


# Authors 
~~~
Developer.: Jaskaran Singh Narula 
~~~ 
