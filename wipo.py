#! /usr/bin/env python

from multiprocessing import Process, Pipe
import subprocess
import re

def scan(pipe):
	re_station_and_strength = re.compile('^.*([0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}) -([0-9]{2}).*$')
	try:
		while True:
			airport_scan = subprocess.check_output(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport', '-s'])
			stations = map( lambda match: (match.group(1), match.group(2)),
					filter( lambda match : match ,
						map( re_station_and_strength.match, airport_scan.split('\n') ) ) )
			pipe.send( stations )
			if not pipe.recv():
				break
	except KeyboardInterrupt as e:
		pass

def main():
	(main_pipe_end, scan_pipe_end) = Pipe()
	scan_process = Process(target=scan, args=(scan_pipe_end,))
	scan_process.start()
	try:
		while True:
			obj = main_pipe_end.recv()
			main_pipe_end.send(True)
			print obj

	except KeyboardInterrupt as e:
		pass
	print '\nTerminating'
	scan_pipe_end.send(None)
	scan_process.join()

main()
