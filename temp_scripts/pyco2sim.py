print("test")
import matlab.engine
from definitions import ROOT_DIR

eng = matlab.engine.start_matlab()

# set_pipeup matlab behind server (only needs to be done on connect(?)
CURRENT_DIR = ROOT_DIR + '\\py2matlabAPI'  # path to store system generated conf files
eng.addpath(CURRENT_DIR, nargout=0)

eng.pyco2sim(nargout=0)
str = 'simnet = {}'.format('ExampleAbsorber')
eng.eval(str, nargout=0)

# getters
prop = 'temp'
pipe = 'P01'
str = """var = simnet.FindPipe("{}").Struct.{};""".format(pipe, prop)
eng.eval(str, nargout=0)
prop_val = eng.eval("var")

# setters
prop = 'temp'
pipe = 'P01'
value = 320
str = """simnet.FindPipe("{}").Stream.FindParameter("{}").ConvValue = {};""".format(pipe, prop, value)
eng.eval(str, nargout=0)
# sovle again
eng.eval('simnet.Solve;', nargout=0)

a = 1
