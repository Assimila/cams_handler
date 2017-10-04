"""
Copyright 2014 Assimila Limited.  All rights reserved

Download CAMS data from the ECMWF data server.

*The user must have registered and the ECMWF API key must be available (e.g. in 
their home directory).*

This code was originally written to support project 2015-01 Newton Agrtech
project with CABI.

LIMITATIONS
- Not all variables are available. To date we have:
        gtco3 : GEMS total column ozone
        aod550 : total aerosol optical depth at 550 nm
        tcwv : total column water vapour
        sf : snowfall
- Designed for surface variables only
"""

from ecmwfapi import ECMWFDataServer


class Query:
    """
    Define the parameters of a call to the ERA Interim data server.

    """
    def __init__(self, var, grid, area, mtype, time, step,
                 start_date, end_date, dformat="netcdf",
                 filename="/media/Data/cams.nc", dataset="cams_nrealtime"):
        """This object defines the parameters of the required ERA Interim data"""

        self.var = var
        self.grid = grid
        self.area = area
        self.type = mtype
        self.filename = filename
        self.start_date = start_date
        self.end_date = end_date
        self.time = time
        self.step = step
        self.format = dformat
        self.dataset = dataset

        self.available_variables = {
            "gtco3": "206.210",
            "aod550": "207.210",
            "tcwv": "137.128",
            "sf": "144.128"
        }

    def download(self):
        """Check defined parameters and download the data"""

        # Prepare parameter to be downloaded
        if isinstance(self.var, basestring):
            self.var = [self.var]
        try:
            variables = [self.available_variables[v] for v in self.var]
        except KeyError as e:
            raise ValueError(
                "Incorrect variable name: {}. Options are {}.".format(
                    e, self.available_variables.keys()))
        param = '/'.join(variables)

        # Prepare date string     
        if self.end_date < self.start_date:
            raise ValueError("Start date must be before end date")
        elif self.end_date == self.start_date:
            date = self.start_date.strftime("%Y-%m-%d")
        else:
            date = self.start_date.strftime("%Y-%m-%d") + "/to/" + \
                   self.end_date.strftime("%Y-%m-%d")

        # Prepare area
        if self.area[0] < self.area[2]:
            raise ValueError("Incorrect area definition. Latitudes incorrect,\
north must be greater than south. Check area_guide for more information.")
        elif self.area[3] > self.area[1]:
            raise ValueError("Incorrect area definition. Longitudes incorrect,\
east must be less than west. Check area_guide for more information.")
        else:
            era_area = [self.area[0], self.area[3], self.area[2], self.area[1]]
            area = '/'.join(map(str, era_area))

        # Prepare grid
        if self.grid not in [3, 2.5, 2, 1.5, 1.125, 1, 0.75, 0.5, 0.25, 0.125]:
            raise ValueError("Incorrect grid resolution. Resolution must be\
one of the following: 3, 2.5, 2, 1.5, 1.125, 1, 0.75, 0.5, 0.25, 0.125")
        else:
            grid = "%s/%s" % (self.grid, self.grid)

        # Check we have been provided with the correct type
        if self.type != "an" and self.type != "fc":
            raise ValueError("Incorrect type. Must be either 'fc' (forecast) \
or 'an' (analysis). Check type_guide for more information")

        # If step or time have been passed as single integers, convert them into lists.
        if isinstance(self.step, int):
            self.step = [self.step]
        if isinstance(self.time, int):
            self.time = [self.time]

        # We need to overwrite the defaults for analysis if only type="an" is passed in
        if self.type == "an" and self.time == [0, 12]:
            self.time = [0, 6, 12, 18]  # Default analysis times

        if self.type == "an" and self.step == [3, 6, 9, 12]:
            self.step = [0]  # Default analysis step

        # Check we have correct times and steps that the ecmwf use
        for thestep in self.step:
            if self.type == "an":
                if thestep not in [0]:
                    raise ValueError("step is {}, must be equal to 0 for type=analysis".format(thestep))
            elif self.type == "fc":
                allowedsteps = [0, 3, 6, 9, 12, 15, 18, 21, 24]
                if thestep not in allowedsteps:
                    raise ValueError("step is {}, must be one of {} for type=forecast".format(thestep, allowedsteps))
        for thetime in self.time:
            if self.type == "an":
                allowedtimes = [0, 6, 12, 18]
                if thetime not in allowedtimes:
                    raise ValueError("time is {}, must be one of {} for type=analysis".format(thetime, allowedtimes))
            elif self.type == "fc":
                allowedtimes = [0, 12]
                if thetime not in allowedtimes:
                    raise ValueError("time is {}, must be one of 00/12 for type=forecast".format(thetime))

        # Prepare times and steps for type analysis
        time = '/'.join([str(t) for t in self.time])
        step = '/'.join([str(s) for s in self.step])

        # lets just print things to check them
        print param, time, step, grid, date, area, self.filename

        # Retrieve the data
        server = ECMWFDataServer()

        server.retrieve({
            'stream': "oper",
            'levtype': "sfc",
            'param': param,
            'dataset': self.dataset,
            'step': step,
            'grid': grid,
            'resol': "av",
            'time': time,
            'date': date,
            'type': self.type,
            'class': "ei",  # This might need to be mc
            'area': area,
            'format': self.format,
            'target': self.filename
        })  # Could be an "expver": "0001", variable
