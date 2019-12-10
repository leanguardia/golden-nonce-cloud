import sys, getopt, time

def arguments(argv, difficulty=None, data="COMSM0010cloud"):
  try: opts, args = getopt.getopt(argv[1:], "hd:a:", ["difficulty=","data="])
  except getopt.GetoptError:
    print('simple_finder.py -d <difficulty> -a <data>')
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print('simple_finder.py -d <difficulty> -a <data>')
      sys.exit()
    elif opt in ("-d", "--difficulty"): difficulty = int(arg)
    elif opt in ("-a", "--data"): data = arg
  return (difficulty, data)