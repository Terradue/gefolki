# gefolki anaconda package

`gefolki, last commit Jan 19, 2019`

GeFolki is a coregistration software that has been developped in the framework of the MEDUSA project, first for SAR/SAR co-registration, then for other cases of remote sensing image coregistration, including hetergeneous image co-registration (ex LIDAR/SAR, optics/SAR, hyperspectral/optics and so on).

### Quick links

* [Prerequisites](#prerequisites)
* [Installation - Ellip Workflows, Ellip Notebook](#installation)
* [Testing: python](#testing_python)
* [Testing: notebook](#testing_notebook)

## <a name="prerequisites">Prerequisites
    
The package is built using `Python 2.7, 3.5, 3.6, 3.7, 3.8`.

## <a name="installation">Installation - Ellip Workflows, Ellip Notebook

Open the terminal and run the following command:

```
sudo conda install gefolki -y
```

## <a name="testing_python">Testing: python
    
Open the terminal and create the input file in the workspace directory:

```
vi /workspace/input_modeling.txt
```

You can copy and paste the *input_modeling_template.txt* as template:

```
###
# Input unwrapped phase (GeoTIFF) 
unw_29047_29222_ortho.tiff
#
# Approx Coordinates fo the co-seismic signal, Lat, Lon 
33.5 73.730
#
# Buffer AOI (degrees)
0.075
#
# Downsampling for speed (0.05-1)
0.2
#
# LOS angles of the satellit (incidence33-43 for S1, azimuth, +15 Descending, -15 Ascending)
40 -15

```
    
Save the file and export the variable *LD_LIBRARY_PATH*:

```
export LD_LIBRARY_PATH=/opt/v94/runtime/glnxa64:/opt/v94/bin/glnxa64:/opt/v94/sys/os/glnxa64:/opt/v94/extern/bin/glnxa64
```

Run the following commands in the shell:

```
python
import run_inverse_model
mr = run_inverse_model.initialize()
mr.run_inverse_model('/workspace/input_modeling.txt', nargout=0)
```

The expected output message should be `run_inverse_model
Function GEOTIFFREAD was unable to find file '/workspace/unw_29047_29222_ortho.tiff'`.

## <a name="testing_notebook">Testing: notebook
    
The package can be used only running python via terminal.
The *subprocess* package is needed in order to start *run_inverse_model*.
    
Open the terminal and create the input file (as already explained in the previous section).
    
Open the notebook. Export the variable *LD_LIBRARY_PATH*:

```
import os
os.environ['LD_LIBRARY_PATH'] = "/opt/v94/runtime/glnxa64:/opt/v94/bin/glnxa64:/opt/v94/sys/os/glnxa64:/opt/v94/extern/bin/glnxa64"
```

Import the *subprocess* and *run_inverse_model* libraries:

```
import subprocess
import run_inverse_model
```

Now test the library:

```
command = 'import run_inverse_model; mr = run_inverse_model.initialize(); mr.run_inverse_model(\"/workspace/input_modeling.txt\", nargout=0)'

options = ['python',
           '-c',
           command,
          ]

p = subprocess.Popen(options,
                     stdout=subprocess.PIPE,
                     stdin=subprocess.PIPE,
                     stderr=subprocess.PIPE)

res, err = p.communicate()

print(res)
print(err)
```

The expected output message should be `run_inverse_model
Function GEOTIFFREAD was unable to find file '/workspace/unw_29047_29222_ortho.tiff'`.

