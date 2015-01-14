* The script is developed to work with smokeping. 
* It accepts 5 arguments name-of-alert, target, loss-pattern, rtt-pattern, hostname. They are all passed by smokeping. http://oss.oetiker.ch/smokeping/doc/smokeping_config.en.html
* To test the script 
"""./mrt_remote.py alert [target ip] loss-pattern rtt-pattern hostname"""
This will test that the mail is being sent and connectivity among the servers.
* Script assumes that ssh connections are passwordless using key authentication.
* The script will log its activity /var/log/smokeping.log
"""
2015-01-14 15:46:27,464 - ALERT has been triggered, alert:alert, target:89.200.142.147, loss:loss-pattern,rtt:rtt-pattern, hostname hostname
2015-01-14 15:46:27,472 - MTR from server1 successful
2015-01-14 15:46:34,728 - MTR from server2 successful
2015-01-14 15:46:39,966 - MTR from server3 successful
"""
