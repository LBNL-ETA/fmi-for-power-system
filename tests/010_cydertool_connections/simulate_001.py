import cydertool

# Compile new FMU
cydertool.compile('pandapower/', 'pandapower')

# Load and run simulation
begin = dt.datetime(2018, 1, 1, 0, 0, 0)
start_s = int((dt.datetime(2018, 6, 17, 3, 0, 0) -
               begin).total_seconds())
end_s = int((dt.datetime(2018, 6, 17, 22, 5, 0) -
             begin).total_seconds())
results = cydertool.simulate(start_s, end_s, 'connections.xlsx')

# Print results
print(results.head())
