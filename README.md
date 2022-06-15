## convertSIGtoEDF
conversion of Brainlab/Schwarzer .SIG files into European Data Format .EDF (EDF+ or BDF+)
- without refiltering
- exports stored events in EDF/BDF
- some header information is also exported in a separate file if not stored in the EDF/BDF already
- currently signals are cut off (flat) at pysical values of +-3277 (EDF) or +-187500 (BDF) giving a resolution of about 0.1 units or 0.02235 units, respetively

**IMPORTANT**: there is a "incl_sens" version that includes the sensitivity information in the header (typically used only for display) to scale the respective channel data. E.g. sensitiviy for EEG channels is 70% that is they are scaled to only 70% of the amplitude. To have the original scaling for the actual recorded micro Volts (or other units) it is recommended **not** to use the "incl_sens" version and use the simple 'no sens' version without that option.

### REQUIREMENTS:
python2.7, linux(/mac)

### TESTED ON:
Ubuntu 18.04 LTS, x64

### INSTALLATION:
```
# install python and pip
sudo apt-get install python
sudo apt-get install python-pip

# intall the repo
git clone https://github.com/Frederik-D-Weber/sigtoedf/
cd sigtoedf
sudo pip install -r requirements.txt
```

### USAGE:
```
python convertSIGtoEDF.py '.../my/sig/file/is/here/XYZ.SIG'
```

### OPTIONAL:
for checking or creating python requirements
```
sudo pip install pipreqs
pipreqs .
```
