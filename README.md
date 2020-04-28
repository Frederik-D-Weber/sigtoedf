## convertSIGtoEDF
conversion of Brainlab/Schwarzer .SIG files into European Data Format .EDF (EDF+ or BDF+)
... without refiltering
... exports stored events in EDF/BDF
... some header information is also exported in a separate file if not stored in the EDF/BDF already
... currently signals are cut off (flat) at pysical values of +-3277 (EDF) or +-187500 (BDF) giving a resolution of about 0.1 units or 0.02235 units, respetively

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
