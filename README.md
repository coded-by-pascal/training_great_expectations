# training_great_expectations


# Setup

## Install
- Python IDE - Empfehlung: Visual Studio Code 
- Python: 3.7 to 3.10
- PIP Packages
- Great Expectations
- virtualenv
- SQL-Client - Empfehlung: DBeaver 

 

## Initialize
### Basic structure
Simple training repo for Great Expectations
```bash
# Create new folder
mkdir tjf_ge_2023-03

# Move to new folder
cd tjf_ge_2023-03

# Clone git repository
git clone https://github.com/coded-by-pascal/training_great_expectations.git
```

### Python environment
```bash
#install virtualenv if not already happen with: pip install virtualenv
#Create a virtual enviorment
virtualenv venv

# activate the virtual enviorment
# for windows
venv\Scripts\activate

#for mac
source venv/bin/activate

# Install requirements
pip install -r training_great_expectations/requirements.txt

# Initialize great expectations
great_expectations init
```

### Expectation
```bash
# Your folder should look like this
├── great_expectations
│   ├── checkpoints
│   ├── expectations
│   ├── great_expectations.yml
│   ├── plugins
│   ├── profilers
│   └── uncommitted
├── training_great_expectations
│   ├── README.md
│   ├── requirements.txt
│   └── testdata
└── venv
    ├── bin
    ├── lib
    └── pyvenv.cfg
```