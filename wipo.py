#! /usr/bin/env python

from multiprocessing import Process, Queue
import subprocess
import re

def scan(q):
	re_station_and_strength = re.compile('^.*([0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}) -([0-9]{2}).*$')
	while True:
		airport_scan = subprocess.check_output(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport', '-s'])
		stations = map( lambda match: (match.group(1), match.group(2)),
				filter( lambda match : match ,
					map( re_station_and_strength.match, airport_scan.split('\n') ) ) )
		print stations

def main():
	q = Queue()
	scan_process = Process(target=scan, args=(q,))
	scan_process.start()
	scan_process.join()

main()
