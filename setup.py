from setuptools import setup, find_packages

consoleScript1 = 'gefolki-mining = gefolki.mining:main'

setup(name="gefolki",
      version="1.0.0",
      description="GeFolki is a coregistration software for SAR/SAR and for other cases of remote sensing image coregistration (ex LIDAR/SAR, optics/SAR, hyperspectral/optics)",
      url="https://github.com/Terradue/gefolki",
      author="Aurelien Plyer, Elise Colin-Koeniguer, Flora Weissgerber et al",
      license="GPL License",
      packages=find_packages(),
      entry_points = {
          'console_scripts': [consoleScript1, ],
      },
      include_package_data=True,
      zip_safe=False)
