"""
Copyright 2014 Assimila Limited.  All rights reserved

Download ERA Interim data from the ECMWF data server. 

*The user must have registered and the ECMWF API key must be available (e.g. in 
their home directory).*

This code was originally written to support project 2015-01 Newton Agrtech
project with CABI.

LIMITATIONS
- Not all variables are available. To date we have: 
        2m temperature
        skin temperature
- Designed for surface variables only
- Designed to download all available timesteps of that type (i.e. all fore
    casting steps or all model steps). Not possible to change this yet.


writen by bethan.perkins@assimila.eu

"""

from ecmwfapi import ECMWFDataServer
import datetime as dt

# Define default start/end dates before initialising the Query object
today = dt.date.today()
default_start = dt.date(today.year-1, today.month, 1)

if default_start.month == 12:
    default_end = dt.date(today.year, 1, 1)
else:
    default_end = dt.date(today.year-1, today.month+1, 1)



class Query:
    """
    Define the parameters of a call to the ERA Interim data server.

    """    
    def __init__(self, var="2m temperature", grid=1, area = [60.0, 
    8.0, 48.0, -13.0], type="fc", time=[0,12], step=[3,6,9,12], 
    start_date=default_start, end_date=default_end, dformat="netcdf",
    filename="/media/Data/cams.nc", dataset="cams_nrealtime"):
        
        "This object defines the parameters of the required ERA Interim data" 
         
        self.var = var
        self.grid = grid
        self.area = area
        self.type = type
        self.filename = filename
        self.start_date = start_date
        self.end_date = end_date
        self.time = time
        self.step = step
        self.format = dformat
        self.dataset = dataset
        
        self.available_variables = {
        "GEMS total column ozone":"206.210", # CAMS
        "total aerosol optical depth at 550 nm":"207.210",
        "total column water vapour":"137.128",
        "snowfall":"144.128"
        }
        self.available_datasets = ['interim', 'era5_test', 'cams_nrealtime']
        self.area_guide = "[N (top), E (right), S (bottom), W (left)]"
        self.type_guide = "Type is 'an' for model re-analysis (output at\
= 00Z, 6Z, 12Z, 18Z). Type is 'fc' for forecast (output at = 3Z 6Z 9Z \
12Z, 15Z 18Z 21Z 24Z)"


        
        if self.dataset not in self.available_datasets:
            raise ValueError("Dataset name must be one of {}".format(self.available_datasets.keys()))

    def download(self):
    
        """Check defined parameters and download the data"""     
        
        # Prepare parameter to be downloaded
        
        # simple string
        if isinstance(self.var, basestring):
            try:
                param = self.available_variables[self.var]
            except:
                raise ValueError("Incorrect variable name. Check \
available_variables for options")

        # tuple
        elif isinstance(self.var, tuple):
             try:
                variables = [self.available_variables[v] for v in self.var]
                param = '/'.join(variables)
             except:
                raise ValueError("Incorrect variable name. Check \
available_variables for options")       
            
        # incorrect type error
        else:
            raise TypeError("Incorrect format for defining parameter. Must be \
a string or a tuple of strings")
            
 

        # Prepare date string     
        if self.end_date < self.start_date:
            raise ValueError("Start date must be before end date")
            
        elif self.end_date == self.start_date:
            date = self.start_date.strftime("%Y-%m-%d")
            
        else:
            date = self.start_date.strftime("%Y-%m-%d")+"/to/"+\
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
            
         # check we have been provided with the correct type  
        if self.type != "an" and self.type != "fc":
            raise ValueError("Incorrect type. Must be either 'fc' (forecast) \
or 'an' (analysis). Check type_guide for more information")

        
        # If step or time have been passed as single integers, convert them 
        # into lists.
        if isinstance(self.step, int):
            self.step = [self.step]
        
        if isinstance(self.time, int):
            self.time = [self.time]
        
        # we need to overwrite the defaults for analysis if only type="an" 
        # is passed in
        if self.type == "an" and self.time == [0,12]:
            self.time = [0, 6, 12, 18] # default analysis times
        
        if self.type == "an" and self.step == [3,6,9,12]:
            self.step = [0] # default analysis step
        
        
        # check we have correct times and steps that the ecmwf use
        for thestep in self.step:
          if self.type == "an":
            if thestep not in [0]:
              raise ValueError("step is %s, must be equal to 0 for type=analysis" % thestep)
          
          elif self.type == "fc":
            allowedsteps =  [0, 3, 6, 9, 12]
            if thestep not in allowedsteps:
              raise ValueError("step is {}, must be one of {} for type=forecast".format(thestep, allowedsteps))
             
        for thetime in self.time:
          if self.type == "an":
            allowedtiems = [0, 6, 12, 18]
            if thetime not in allowedtimes:
              raise ValueError("time is {}, must be one of {} for type=analysis".format(thetime, allowedtimes))
          
          elif self.type == "fc":
            allowedtimes = [0, 12]
            if thetime not in allowedtimes:
              raise ValueError("time is %s, must be one of 00/12 for type=forecast" % thetime)
              
        # Prepare times and steps for type analysis
        time = '/'.join([str(t) for t in self.time])
        step = '/'.join([str(s) for s in self.step])
        
        # lets just print things to check them
        print param, time, step, grid, date, area, self.filename

        # Retrieve the data
        server = ECMWFDataServer()
        
        server.retrieve({
            'stream' : "oper",
            'levtype' : "sfc",
            'param' : param,
            'dataset' : self.dataset,
            'step' : step,
            'grid' : grid,
            'resol' : "av",
            'time' : time,
            'date' : date,
            'type' : self.type,
            'class' : "ei",
            'area' : area,
            'format' : self.format,
            'target' : self.filename           
        })
        

