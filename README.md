# training_great_expectations


# Setup
export sf_user=VORNAME_NACHNAME
export sf_password"MY_SECRET_PASSWORD



## Install

*  Python IDE
    - Empfehlung: Visual Studio Code 
* Python: 
    - 3.8 to 3.11
* PIP Packages
    - Great Expectations

 
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

### Expectation
```bash
# Your folder should look like this
tjf_ge_2023-03
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