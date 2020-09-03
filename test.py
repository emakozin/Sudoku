import json
import os

here = os.path.dirname(os.path.abspath(__file__))

filename = os.path.join(here, 'primer_lahek' )
f = open(filename,"rb")
data = json.load(f) 
for i in data['emp_details']: 
    print(i) 
f.close() 



