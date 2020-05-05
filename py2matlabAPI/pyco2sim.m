% pyco2sim
% matlab script that sets paths and adds location of flowsheets
% server side

% location of co2sim
cd 'C:\Users\ft\Desktop\visha\CO2SIM_lite\CO2SIM_lite\co2sim_matlab'
flowsheetspath = 'C:\Users\ft\Desktop\visha\CO2SIM_lite\CO2SIM_lite'

settingpath
addpath(flowsheetspath)


% simnet = ExampleAbsorber;
% simnet.Solve;
% simnet.PrintStreams;