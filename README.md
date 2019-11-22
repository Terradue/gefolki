# gefolki anaconda package

`gefolki, last commit Jan 19, 2019`

GeFolki is a coregistration software that has been developped in the framework of the MEDUSA project, first for SAR/SAR co-registration, then for other cases of remote sensing image coregistration, including hetergeneous image co-registration (ex LIDAR/SAR, optics/SAR, hyperspectral/optics and so on).

### Quick links

* [Prerequisites](#prerequisites)
* [Installation - Ellip Workflows, Ellip Notebook](#installation)
* [Demo: notebook](#demo_notebook)

## <a name="prerequisites">Prerequisites
    
The package is built using `Python 2.7, 3.5, 3.6, 3.7, 3.8`.

## <a name="installation">Installation - Ellip Workflows, Ellip Notebook

Open the terminal and run the following command:

```
sudo conda install gefolki -y
```

## <a name="demo_notebook">Demo: notebook
    
Open the notebook and import the package:

```
import gefolki
```

Download these images to run the demo:

```
!mkdir ./datasets
!wget "https://raw.githubusercontent.com/aplyer/gefolki/master/datasets/radar_bandep.png" -P ./datasets/
!wget "https://raw.githubusercontent.com/aplyer/gefolki/master/datasets/lidar_georef.png" -P ./datasets/
!wget "https://raw.githubusercontent.com/aplyer/gefolki/master/datasets/optiquehr_georef.png" -P ./datasets/
```

New run the demo:

```
gefolki.demo()
```