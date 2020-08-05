from client.RestAPI import RESTApi
import pandas as pd
import psutil
import os
from collections import namedtuple
from datetime import datetime
import logging
from definitions import create_dir_if_not_exist, TEMP_DIR

_LOG = logging.getLogger(__name__)

# run this to start logging
logging.debug("Begin")
_LOG.setLevel(logging.DEBUG)


def f_cost(obj, duty, cost_spec, df, datafile, result_ucurve):
    """
    runs a simulation to find current cost function
    """

    # set new duty
    obj.set_unit('Reboiler', 'flashQ', duty * 3600)
    # solve flowsheet
    obj.solve()
    # get object function
    o = get_summary_data(obj, bypass=False)
    # objectbfunction
    costfunc = cost_spec - (o['capture_rate']) / 100.0

    # optionally save the data to file
    _, err_bounds = check_save_results(df, datafile, result_ucurve, obj)

    return costfunc, err_bounds


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def optimize(f, x0, epsilon, cost_spec, obj, df, datafile, result_ucurve):
    # implementering av newtons metode med step-control
    maxiter = 12
    verbose = True
    err_i = 1
    stepsize = .2  # 15 percent increment on iterator (duty) higher is more agressive on the solvers
    setpsizecontrol = True
    idx = 0
    # bruker normaliserte verdier inn i iterator
    first_guess = 1.0
    x_i = first_guess
    f_i, error = f(obj, x_i * x0, cost_spec, df, datafile, result_ucurve)
    x_i_1 = x_i + first_guess * 0.05
    Dx = x_i_1 - x_i

    while err_i > epsilon and idx < maxiter:
        f_i_1, error = f(obj, x_i_1 * x0, cost_spec, df, datafile, result_ucurve)
        err_i = abs(f_i_1 + f_i)
        relerr_i = 1 - (abs(f_i_1) / abs(f_i))
        fdot = (f_i_1 - f_i) / (x_i_1 - x_i)
        xNR = x_i_1 - f_i_1 / fdot
        x_i = x_i_1

        if setpsizecontrol is True:
            next_deltastep = xNR - x_i_1
            controlled_deltastep = stepsize
            if abs(next_deltastep) < controlled_deltastep:
                x_i_1_ = xNR
            else:
                _LOG.debug('entering step control {:<20f} kW'.format(abs(next_deltastep * x0)))
                if next_deltastep < 0:
                    x_i_1_ = x_i_1 - x_i_1 * stepsize
                else:
                    x_i_1_ = x_i_1 + x_i_1 * stepsize
        else:
            x_i_1_ = xNR

        x_i_1 = x_i_1_
        f_i = f_i_1
        idx = idx + 1

        # check if error in simulation
        if error == 1:
            # reduce with 25% to get out of the zone
            obj.set_unit('Reboiler', 'flashQ', x0 * 0.75 * 3600)
            break

        if error == 2:
            # reduce with 25% to get out of the zone
            obj.set_unit('Reboiler', 'flashQ', x0 * 1.2 * 3600)
            break

        if verbose is True:
            _LOG.debug('iterations {:<20f}'.format(idx))
            _LOG.debug('current residual: {:<20f}'.format(f_i_1))
            _LOG.debug('current cost function: {:<20f}'.format(err_i))
            _LOG.debug('un-normalized manipulated var: {:<20f}'.format(x_i_1 * x0))

    _LOG.debug(' error:  {:<20f}'.format(error))
    _LOG.debug(' system finished w/ abs. error:  {:<20f}'.format(err_i))
    _LOG.debug(' rel. error:  {:<20f}'.format(relerr_i))
    _LOG.debug(' object func. at root:  {:<20f}'.format(f_i_1))


    return err_i


def get_ram_situation():
    print('cpu_percent (local) {}'.format(psutil.cpu_percent()))
    d = dict(psutil.virtual_memory()._asdict())
    print('virtual memory percent (local) {}'.format(d['percent']))


def get_summary_data(obj, bypass):
    # # define some locals
    #     # pipe_v1 = 'V1'
    #     # pipe_v2 = 'V2'
    #     # unit_reb = 'Reboiler'
    #     # pipe_lean = 'P09'
    #     # pipe_rich = 'P03'
    #     # unit_control = 'Con01'
    #     # unit_absorber = 'Abs_col'
    #     #
    #     # if bypass:
    #     #     # inVapCO2 = -1
    #     #     # outVapCO2 = -1
    #     #     reboilerDuty = -1
    #     #     fluegas_CO2 = -1
    #     #     fluegas_temp = -1
    #     #     absorber_height = -1
    #     #     solvent_circ_rate = -1
    #     #     capture_rate = -1
    #     #     reboiler_temp = -1
    #     #     lean_loading = -1
    #     #     richLoading = -1
    #     #     srd = -1
    #     #     timestamp = -1
    #     # else:
    #     #     pobj_in = obj.get_pipe_struct(pipe_v1)
    #     #     ipy_co2 = int(float(pobj_in['componentlocations']['CO2'])) - 1
    #     #     ipy_mea = int(float(pobj_in['componentlocations']['MEA'])) - 1
    #     #     inVapCO2 = float(pobj_in['flow']) * pobj_in['molfrac'][ipy_co2]
    #     #     pobj_out = obj.get_pipe_struct(pipe_v2)
    #     #     outVapCO2 = float(pobj_out['flow']) * pobj_out['molfrac'][ipy_co2]
    #     #     leanObj = obj.get_pipe_struct(pipe_lean)
    #     #     richObj = obj.get_pipe_struct(pipe_rich)
    #     #     reboiler_duty = obj.get_unit(unit_reb, 'flashQ') / 3600  # kW
    #     #     reboiler_temp = obj.get_unit(unit_reb, 'flashT') - 273.15
    #     #
    #     #     fluegas_CO2 = pobj_in['molfrac'][0]
    #     #     fluegas_temp = obj.get_pipe(pipe_v1, 'temp') - 273.15  # C
    #     #     absorber_height = obj.get_unit(unit_absorber, 'length')
    #     #     solvent_circ_rate = obj.get_unit(unit_control, 'flow')
    #     #     capture_rate = (1 - outVapCO2 / inVapCO2) * 100
    #     #     lean_loading = leanObj['molfrac'][ipy_co2] / leanObj['molfrac'][ipy_mea]
    #     #     richLoading = richObj['molfrac'][ipy_co2] / richObj['molfrac'][ipy_mea]
    #     #     try:
    #     #         srd = (reboilerDuty * 3600) / ((inVapCO2 - outVapCO2) * 44) / 1000
    #     #     except ZeroDivisionError:
    #     #         print("b value is zero")
    #     #         srd = -1
    if not bypass:
        struct= obj.get_summary_struct()
        # convert all to float
        for k, v in struct.items():
            struct[k] = float(v)

        timestamp = get_timestamp()

    # Inputs:
    # Outputs:
        parameters = {'fluegas_CO2': struct['fluegas_CO2'], 'fluegas_temp': struct['fluegas_temp'], 'absorber_height': struct['absorber_height'],
                      'reboiler_duty': struct['reboiler_duty'], 'solvent_circ_rate': struct['solvent_circ_rate'],
                      'capture_rate': struct['capture_rate'], 'reboiler_temp': struct['reboiler_temp'], 'lean_loading': struct['lean_loading'],
                      'richLoading': struct['richLoading'], 'srd': struct['srd'], 'timestamp': timestamp}
    else:
        parameters = {'fluegas_CO2': -1, 'fluegas_temp': -1, 'absorber_height': -1,
                  'reboiler_duty': -1, 'solvent_circ_rate': -1,
                  'capture_rate': -1, 'reboiler_temp': -1, 'lean_loading': -1,
                  'richLoading': -1, 'srd': -1, 'timestamp': -1}

    # display summary
    # verbose = False
    # if verbose:
    #     print('*' * 50)
    #     print('Absorber height:         {:<20f} m'.format(absorber_height))
    #     print('Fluegas CO2:             {:<20f} vol%'.format(fluegas_CO2 * 100))
    #     print('Fluegas temp:            {:<20f} C'.format(fluegas_temp))
    #     print('Solvent circulation rate:{:<20f} l/min'.format(solvent_circ_rate))
    #     print('Percent Removed:         {:<20f}'.format(capture_rate))
    #     print('Reboiler duty:           {:<20f} kW'.format(reboilerDuty))
    #     print('Reboiler temp:           {:<20f} C'.format(reboiler_temp))
    #     print('Lean Loading:            {:<20f}'.format(lean_loading))
    #     print('Rich Loading:            {:<20f}'.format(richLoading))
    #     print('SRD:                     {:<20f} GJ/kg CO2 removed'.format(srd))
    #     print('*' * 50)

    return parameters


def check_save_results(df, datafile, result_ucurve, obj):
    # we only want to write a placeholder, not actual values
    result = pd.DataFrame(columns=[*get_summary_data(obj=obj, bypass=True)])
    # write the actual results
    o = get_summary_data(obj, bypass=False)
    result = result.append(o, ignore_index=True)
    _LOG.debug('Writing to matrix file:')
    result.to_csv(datafile, mode='a', header=False, index=False)

    result_ucurve = result_ucurve.append(result, ignore_index=True)
    print(result_ucurve.to_string())
    err_bounds = 0

    # check within loading range
    if 0.10 <= o['lean_loading'] <= 0.38:
        pass
    else:
        err_bounds = 1

    #check within reboiler range
    if o['reboiler_duty'] < 5.5:
        err_bounds = 2

    if err_bounds != 0:
        _LOG.debug('Lean loading too low or high for MEA, exiting current run: {}'.format(err_bounds))

    return result_ucurve, err_bounds


def u_curve(obj, olddata, flowrange, fluegas_co2, height, duty, capture, fluegas_temp, datafile, ia):
    """
    Varies solvent circulation rate.
    """
    df = olddata  # Previously stored simulations
    result_ucurve = pd.DataFrame()  # Dataframe for storing all results
    idy = 0  # intern teller
    for flow in flowrange:
        exist = False
        discard_isTrue = False
        isTrue = False
        for i in df.index:
            if ia.is_optimize_true:
                isTrue = abs(df.iloc[i]['capture_rate'] - ia.capturerange[idy]*100) < 0.1 and \
                        df.iloc[i]['fluegas_CO2'] == fluegas_co2 and \
                        df.iloc[i]['absorber_height'] == height and \
                        abs(df.iloc[i]['solvent_circ_rate'] - flow) < 3.0 and \
                        abs(df.iloc[i]['fluegas_temp'] - (fluegas_temp - 273.13)) < 3.0
                # if not 0.10 <= df.iloc[i]['lean_loading'] <= 0.38:
                #     discard_isTrue = True
            else:
                isTrue = df.iloc[i]['reboiler_duty'] == duty and \
                         df.iloc[i]['fluegas_CO2'] == fluegas_co2 and \
                         df.iloc[i]['absorber_height'] == height and \
                         abs(df.iloc[i]['solvent_circ_rate'] - flow) < 3.0 and \
                         abs(df.iloc[i]['fluegas_temp'] - (fluegas_temp - 273.13)) < 3.0
                # if not 0.10 <= df.iloc[i]['lean_loading'] <= 0.38:
                #     discard_isTrue = True

            if isTrue: #and discard_isTrue is False:
                exist = True
                _LOG.debug(
                    f'Simulation with solvent recirc. rate = {flow} l/min., height:{height}, '
                    f'Duty: {duty}, CO2:{fluegas_co2}, Fluegas temp {fluegas_temp}C, capture rate {ia.capturerange[idy]*100} already exists:')
                if exist is True:
                     break

        if not exist:
            _LOG.debug('New case for simulation:')

            get_ram_situation()

            # set new flowrate
            obj.set_unit('Con01', 'flow', flow)

            print(
                f'Simulating with solvent recirc. rate = {flow} l/min., '
                f'height:{height}, Duty: {duty}, CO2:{fluegas_co2}')

            if ia.is_optimize_true:
                print(f'Simulating to target capture of {capture} %.')
                optimize(f=f_cost, x0=duty, epsilon=1e-3, cost_spec=capture, obj=obj,
                         df=df, datafile=datafile, result_ucurve=result_ucurve)
            else:
                obj.solve()
                result_ucurve, error = check_save_results(df, datafile, result_ucurve, obj)
                # check if error in simulation (bounds impeeding progress)
                if error is True:
                    break

            idy += 1


def ant_miner(obj, datafile, flowsheetrestart, url, ia):
    if not os.path.exists(datafile):
        with open(datafile, 'w'):
            result = pd.DataFrame(columns=[*get_summary_data(obj=obj, bypass=True)])
            result = result.append(get_summary_data(obj, bypass=True), ignore_index=True)
            result.to_csv(datafile, mode='a', header=False, index=False)

    df = pd.read_csv(datafile)  # Previously performed simulations

    # FIXME (hardcoding)
    frac_inert = 1.0 - ia.frac_h20

    # total nr of runs
    nr_runs = len(ia.heightrange) * len(ia.fluegasco2range) * len(ia.dutyrange) * len(ia.flowrange)

    _LOG.debug(' total number of runs: {}'.format(nr_runs))
    """ Kjører u-kurver for ulike co2-kons, duties og pakningshøyder """
    idx = 0
    idx_f = 0
    idx_d = 0
    for height in ia.heightrange:
        for fluegas_co2 in ia.fluegasco2range:

            # reverses and alternates array depending on odd or even number
            if idx_d % 2 == 0:
                dutyrange_ = ia.dutyrange
                capturerange_ = ia.capturerange
            elif idx_d % 2 == 1:
                dutyrange_ = ia.dutyrange[::-1]
                capturerange_ = ia.capturerange[::-1]

            for i, duty in enumerate(dutyrange_):
                if ia.is_optimize_true is True:
                    # provide initial guess for the optimizer
                    duty = obj.get_unit('Reboiler', 'flashQ') / 3600.  # kW
                    capture = capturerange_[i]
                else:
                    # we set according to matrix
                    obj.set_unit('Reboiler', 'flashQ', duty * 3600)  # convert to kJ/h
                # Set current case
                obj.set_unit('Abs_col', 'length', height)

                # set fluegas_temperature (kan ikke denne settes ved input til løkke)
                fluegas_temp = ia.fluegas_temp
                obj.set_pipe('V1', 'temp', fluegas_temp)

                # NB: kun gydlig for MEA pakke med 5 komponenter
                molfrac_tup = (fluegas_co2, ia.frac_h20, 0.0, 0.0, frac_inert - fluegas_co2)
                checksum = sum(molfrac_tup)
                obj.set_pipe_components('V1', molfrac_tup)

                # partall
                if idx_f % 2 == 0:
                    flowrange = ia.flowrange
                elif idx_f % 2 == 1:
                    flowrange = ia.flowrange[::-1]

                u_curve(obj=obj, olddata=df, flowrange=flowrange, fluegas_co2=fluegas_co2,
                        height=height, duty=duty, capture=capture, fluegas_temp=fluegas_temp, datafile=datafile, ia=ia)

                idx += 1
                idx_f += 1
                idx_d += 1

                # number of simulations before refresh ram
                nr_u_curves = 20
                _LOG.debug('Simulations before refresh ram: {}'.format(nr_u_curves-idx))
                # relaster casefile, ikke ideelt, hensikt for å rense ram
                # alternativt: simnet.save("navn") lagrer også casefile med siste versdier
                if idx == nr_u_curves:
                    flowsheet = 'ExampleAbsorber'
                    obj = RESTApi(url, flowsheet)
                    obj.connect()
                    obj = RESTApi(url, flowsheetrestart)
                    obj.connect()
                    _LOG.debug('Reloaded Matlab engine')
                    # resett teller
                    idx = 0


def run_miner():
    url = "http://localhost:5001/"
    # url = "http://178.164.32.34:5001/"
    flowsheet = 'ExampleTillerClosedLoop_val_orig_astarita_ng'
    obj = RESTApi(url, flowsheet)
    obj.connect()
    filename = 'matrix_90_20_temp_in_48C_2.csv'

    # setup a folder to store these files
    create_dir_if_not_exist(TEMP_DIR)
    abs_filename = TEMP_DIR + '/' + filename
    # create if not exist
    if not os.path.exists(abs_filename):
        with open(abs_filename, 'w+'):
            pass
        # create initial header columns
        res = pd.DataFrame(columns=[*get_summary_data(obj=obj, bypass=True)])
        res.to_csv(abs_filename, mode='a', header=True, index=False)

    ia = namedtuple('Matrix_input',
                    ['is_optimize_true',
                     'flowrange',
                     'fluegasco2range',
                     'dutyrange',
                     'heightrange',
                     'frac_h20',
                     'fluegas_temp'
                     ])

    # choose wether targeting a capture rate or running free, True-run optimizer, False-feed forward and no capturerange
    ia.is_optimize_true = True
    ia.heightrange = [20., 15.] #, 10.]
    ia.fluegasco2range = [0.06]# , 0.05, 0.04, 0.03, 0.02, 0.01]  # mol% ("wet")
    ia.dutyrange = [14., 12.]#, 10., 1,1,1,1,1]  # kW #not used if optimizer is  used
    ia.flowrange = [22., 20., 14., 16., 18.]  # U-curve circulation rates kmol/h
    # ia.capturerange = [.90, .85, .80, .75, .70, .65, .60]
    # ia.capturerange = [.60, .50, .40, .30, .20]
    #ia.capturerange = [.90, .80, .70]  # percent note, size of vector must be same as dutyrange
    ia.capturerange = [.90, .80] #, .70, .60, .50, .40, .30, .20]  # percent note, size of vector must be same as dutyrange
    ia.frac_h20 = 0.042271  # saturation water concentration FIXME
    ia.fluegas_temp = 48.0 + 273.15 #K

    assert (len(ia.dutyrange) == len(ia.capturerange))
    # run the miner
    ant_miner(obj=obj, datafile=abs_filename, flowsheetrestart=flowsheet, url=url, ia=ia)


if __name__ == '__main__':
    run_miner()
