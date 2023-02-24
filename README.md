# training_great_expectations


# Setup

## Install
- Python IDE - Empfehlung: Visual Studio Code 
- Python: 3.7 to 3.10
- PIP Packages
- Great Expectations
- Venv
- SQL-Client - Empfehlung: DBeaver 

 

## Initialize
### Basic structure
Simple training repo for Great Expectations
```shell
# Create new folder
mkdir tjf_ge_2023-03

# Move to new folder
cd tjf_ge_2023-03

# Clone git repository
git clone https://github.com/coded-by-pascal/training_great_expectations.git

# Initialize great expectations
great_expectations init
```

### Python environment
```shell
python -m tjf_ge

source tjf_ge/bin/activate

pip install -r requirements.txt
```