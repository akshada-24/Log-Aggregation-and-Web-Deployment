from programs import samelogs_function
#from programs import rsyslogd_function
#from programs import NetworkManagerlog_function


def main_func(log_name, log_date, log_keyword, s3Buc):
	print("in maincode_function.main_fun()")
	list1=["avahi-daemon.log", "CROND.log", "dhclient.log", "anacron.log", "chronyd.log","dbus.log","systemd.log","dbus.log"]
	#os.chdir(r'.\..\LOGS_PROJECT\Dates')
	if log_name in list1:
		samelogs_function.f1(log_name, log_date, log_keyword, s3Buc)
	else:
		print("log name is not in the list")