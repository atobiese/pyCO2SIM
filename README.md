
## Running simulations on a server with OpenAPI (swagger)


### Built With

* [Python 3]()
* [Matlab]()
* [CO2SIM]()

### Install

Installing python code with pipenv. Clone repo pyCO2SIM
```sh
git clone https://github.com/atobiese/pyCO2SIM.git
cd pyCO2SIM
pipenv install
```

NB: Installing matlab engine requires installed matlab on host pc:

How to install matlab engine in pipenv:
1. Open shell as administrator, in cmd shell, open the virtual environment:
```sh
cd C:\repos\github\pyCO2SIM
pipenv shell
```
you are now inside the virtual environment

2. from [here](https://se.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html):
```
cd "matlabroot\extern\engines\python"
```
where matlabroot can be found by typing:
``` matlabroot ```

ans =

    'C:\Program Files\MATLAB\R2019b'

so:
```
cd C:\Program Files\MATLAB\R2019b\extern\engines\python"
python setup.py install
```
The matlab engine should now work in python fex:
```
import matlab.engine
eng = matlab.engine.start_matlab()
```

### Prerequisites


* Python 
* Matlab 

## Usage

The server will enble running matlab code by instantiating a simulator wich can be accesssed through the api from the client folder. 
1. First start the server by running server.py 
2. Then run co2sim_dataminer.py. The code stores results in a csv-file and can be analyzed with the co2sim_dataminer_analysis.py script. 


_For more examples, please refer to the [Documentation]()_


[![logo][img1]]()

## Authors

Andrew Tobiesen and Aslak Einbu

## License



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[img1]: server/static/images/flowsheet.png

