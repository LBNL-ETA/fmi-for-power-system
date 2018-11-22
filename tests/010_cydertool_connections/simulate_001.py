from cydertool import compile as cyderc
from cydertool import simulate as cyders

# Compile new FMU
cyderc.compile('pandapower/', 'pandapower')

# Load and run simulation
begin = dt.datetime(2018, 1, 1, 0, 0, 0)
start_s = int((dt.datetime(2018, 6, 17, 3, 0, 0) -
               begin).total_seconds())
end_s = int((dt.datetime(2018, 6, 17, 22, 5, 0) -
             begin).total_seconds())
results = cyders.simulate(start_s, end_s, 'connections.xlsx')

# Print results
print(results.head())
