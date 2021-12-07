<h1 align="center">Elevation-based Navigation</h1>
EleNa(Elevation-based Navigation) is a routing software that helps users calculate a route based on their preferences. Users are able to choose between getting a route with higher elevation or one with lower elevation. If the user wants a time-constrained workout, they might want a path with the highest elevation. If the user rather go an extra mile to avoid path with a huge elevation gain, then they will want to choose the lower elevation choice.


<!-- TABLE OF CONTENTS -->

## Table of Contents

- [Getting Started](#starting)
- [Contributing](#contribute)


<!-- GETTING STARTED -->

<a name="starting"></a>
## Getting Started

To get a local copy up and running follow these steps.

1. git clone the repo
2. cd Elena/elena-frontend
3. npm install
4. yarn start to start up frontend
5. Download Anaconda prompt https://www.anaconda.com/products/individual 
6. Open Anaconda prompt and cd Elena/server
7. run conda config --prepend channels conda-forge
8. run conda create -n ox --strict-channel-priority osmnx
9. run conda activate ox
10. run pip install flask
11. run python index.py to startup backend server locally


<!-- CONTRIBUTING -->

<a name="contribute"></a>
## Contributing

For team mates to contribute follow these steps.

2. Add your changes to the staging area (`git add .`)
3. Commit your Changes (`git commit -m "insert commnet about changes"`)
4. Push (`git push`)





