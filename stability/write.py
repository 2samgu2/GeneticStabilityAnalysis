import numpy as np
import json as js
from os.path import isfile


def writeFile ( info_name, info_data, data_name, data ):

    if ( not isfile( info_name ) and not isfile( data_name ) ):
        with open( info_name, 'w' ) as f:
            for d in info_data:
                f.write( js.dumps( d, f ) )
                f.write( "\n" )
        data = np.array(data)
        np.save(data_name, data)
    else:
        print ("Could not create file.  Please check if file exists and re-run")