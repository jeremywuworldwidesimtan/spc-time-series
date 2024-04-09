import subprocess, datetime, configparser, os

if __name__ == '__main__':
   # Who cares about multithreading if u use nampi array and did a few mods u will get slightly faster speeds
   conf = configparser.ConfigParser()
   conf.read('config.ini')

   custom_toggle = conf['main'].getboolean('customfilename_toggle')
   date_time = datetime.datetime.now().strftime('%Y.%m.%d-%H.%M.%S.%f')
   if custom_toggle:
      if conf['main']['customfilename_data'] != '':
         data = conf['main']['customfilename_data'] + ".csv"
      else:
         data = "data.csv"

      if conf['main']['customfilename_log'] != '':
         log = conf['main']['customfilename_log'] + ".txt"
      else:
         log = "log.txt"
   else:
      if conf['main']['prefix'] != '':
         pref = conf['main']['prefix']
         data = f"{pref}-" + date_time + ".csv"
         log = f"{pref}_LOG-" + date_time + ".txt"
      else:
         data = f"DATA-" + date_time + ".csv"
         log = f"LOG-" + date_time + ".txt"
   seed = int(conf['generator']['seed'])
   if os.path.exists(data):
      print(data, "loaded")
   else:
      print(data, "created")
      open(data, 'x')

   if os.path.exists(log):
      print(log, "loaded")
   else:
      print(log, "created")
      open(log, 'x')
   rate = float(conf['main']['rate'])
   rate = rate * 1000 # most libraries and functions use miliseconds

   if int(conf['generator']['min']) < int(conf['generator']['max']):
      minv = int(conf['generator']['min'])
      maxv = int(conf['generator']['max'])
   else:
      maxv = int(conf['generator']['min'])
      minv = int(conf['generator']['max'])

   commands = [
      f'python generator.py {data} {rate} {seed} {minv} {maxv}',
      f'python spcmonitor.py {data} {rate} {log}',
      f'python logsviewer.py {log}',
      f'python extendedmonitor.py {data} {rate} {log}'
   ] if conf['generator'].getboolean('enable') else [
      f'python spcmonitor.py {data} {rate} {log}',
      f'python logsviewer.py {log}',
      f'python extendedmonitor.py {data} {rate} {log}'
   ]

   procs = [ subprocess.Popen(i) for i in commands ]
   for p in procs:
      p.wait()