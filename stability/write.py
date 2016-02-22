"""write.py.

Author -- Terek R Arce
Version -- 1.0

Copyright 2016 Terek Arce

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

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
