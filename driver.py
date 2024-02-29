import subprocess, datetime
date_time = datetime.datetime.now().strftime('%Y.%m.%d-%H.%M.%S.%f')
data = "JBF-" + date_time + ".csv"
log = "JBFlog-" + date_time + ".txt"
open(data, 'x')
open(log, 'x')
rate = 0.5
rate = rate * 1000 # most libraries and functions use miliseconds

commands = [
   f'python generator.py {data} {rate}',
   f'python spcmonitor.py {data} {rate} {log}',
   f'python logsviewer.py {log}'
]

procs = [ subprocess.Popen(i) for i in commands ]
for p in procs:
   p.wait()
