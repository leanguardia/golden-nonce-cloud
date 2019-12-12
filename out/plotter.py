import pandas as pd
import matplotlib.pyplot as plt

def simple_finder_performance():
  data = pd.read_csv('out/simple-finder.csv', delim_whitespace=True)
  is_local = data['env'] == 'local'
  is_finder_1 = data['finder'] == 1
  local_1 = data[is_local & is_finder_1]
  is_finder_2 = data['finder'] == 2
  local_2 = data[is_local & is_finder_2]
  difficulty = range(1, 8)
  plt.plot(difficulty, local_1['seconds'], label="Finder 1")
  plt.plot(difficulty, local_2['seconds'], label="Finder 2")
  plt.xlabel('Difficulty')
  plt.ylabel('Seconds')
  plt.title("Local Finders")
  plt.legend()
  plt.savefig("out/performance-local-finder.png")

if __name__ == "__main__":
  simple_finder_performance()
  # cloud_finder_performance()