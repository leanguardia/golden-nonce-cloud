import sys, getopt, time

def arguments(argv, num_of_workers=1, difficulty=None, data="COMSM0010cloud"):
  try:
    opts, args = getopt.getopt(
      argv[1:],
      "hd:a:n:",
      ["difficulty=","data=", "num_of_workers="]
    )
  except getopt.GetoptError:
    print('cnd.py -n <num_of_workers> -d <difficulty> -a <data>')
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print('cnd.py -n <num_of_workers> -d <difficulty> -a <data>')
      sys.exit()
    elif opt in ("-n", "--num_of_workers"): num_of_workers = int(arg) or num_of_workers
    elif opt in ("-d", "--difficulty"): difficulty = int(arg)
    elif opt in ("-a", "--data"): data = arg or data
  if(not difficulty or not data or not num_of_workers):
    raise ValueError("Missing parameters: -n or -d")
  return (num_of_workers, difficulty, data)
