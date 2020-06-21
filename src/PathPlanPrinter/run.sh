
source ./env/bin/activate
for heuristic in 'manhattan' 'euclidean' 'octile' 'dijkstra' 'chebyshev'; do
  for algorithm in 'A*' 'theta'; do
    python ./src/run_path_planning.py \
      --scenario ./res/map2.png \
      --start "(3,3)" \
      --finish "(36,36)" \
      --grid_size "(40,40)" \
      --algorithm $algorithm      `# Dijkstra  || A* || theta`\
      --heuristic $heuristic   `# manhattan || naive || euclidean || octile || dijkstra || chebyshev`\
      --scale 1.001 \
      --out ./out/task7Path-$algorithm-$heuristic-scaled.png
  done
done
deactivate