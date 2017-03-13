For Lillie
======

Create a script that:
-------

  1. Pulls all data (.VEC files)
  2. Processes data
     - Loads .VEC file
     - Cleans data
     - Motion corrects data
     - Rotates to 'principal axes'
     - Saves this data to a .h5 file
     - 'bins' the data
     - Save the 'bin' data to a .h5 file
  3. Plots basic results (time series, and spectra)
     - The figures should be saved to a folder inside of the
       repository.
  
  Each of the items above should be their own module. Build one of them at a time. The `main.py` script should sit in the home directory, and import the above modules, and have a function `run()` or `main()` that runs the steps above as three commands, e.g., `pull_data()`, `process_data()`, `plot_results()`.

Create outline
-------

Create an outline of a poster, and place the file in this repo (I like
powerpoint, find a 'poster template'). I think it should include:

- short intro section
  - this is tidal energy, this is how much there is in the U.S., tidal channel turbulence is important because...
- What ADVs are, and what moored ADV measurements are, description of `IMU`
- Basic timeseries of tidal channel velocity, and 'tidal power density'
- Basic timeseries of turbulence statistics
- What you did: 
  1. Fit statistics of measurements
  2. Input to statistical tool for simulating turbulence
  3. This lowers the cost of estimating device loads (lifetimes), an important variable in LCOE
- histograms of statistics and/or plots of spectra (with fits)
- Conclusion section
  - This is all important for creating simulation tools that help
    engineers design devices that lower LCOE
  - Other?

For Levi
======

Questions?
