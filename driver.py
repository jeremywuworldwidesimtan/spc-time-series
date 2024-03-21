import subprocess, datetime, configparser

if __name__ == '__main__':
   # Who cares about multithreading if u use nampi array and did a few mods u will get slightly faster speeds
   conf = configparser.ConfigParser()
   conf.read('config.ini')

   custom_toggle = conf['main'].getboolean('customfilename_toggle')
   date_time = datetime.datetime.now().strftime('%Y.%m.%d-%H.%M.%S.%f')
   if custom_toggle:
      data = conf['main']['customfilename_data'] + ".csv"
      log = conf['main']['customfilename_log'] + ".txt"
   else:
      pref = conf['main']['prefix']
      data = f"{pref}-" + date_time + ".csv"
      log = f"{pref}_LOG-" + date_time + ".txt"
   seed = int(conf['generator']['seed'])
   open(data, 'x')
   open(log, 'x')
   rate = float(conf['main']['rate'])
   rate = rate * 1000 # most libraries and functions use miliseconds

   commands = [
      f'python generator.py {data} {rate} {seed}',
      f'python spcmonitor.py {data} {rate} {log}',
      f'python logsviewer.py {log}',
      f'python extendedmonitor.py {data} {rate} {log}'
   ]

   procs = [ subprocess.Popen(i) for i in commands ]
   for p in procs:
      p.wait()