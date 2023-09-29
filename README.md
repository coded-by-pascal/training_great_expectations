# training_great_expectations

## Voraussetzungen

- Python IDE
    - Empfehlung: Visual Studio Code oder [VSCodium](https://vscodium.com/)
    - [NeoVim](https://neovim.io/)
- [Python](https://www.python.org/)
    - 3.8 to 3.11
- PIP Packages
    - [Great Expectations](https://pypi.org/project/great-expectations/)

## Initialize

### Basic structure

Store credentials in environment variables.
Note: Do this in every new terminal session or use some tool like [direnv](https://direnv.net/)
```bash
export sf_user="VORNAME_NACHNAME"
export sf_password="MY_SECRET_PASSWORD"
```

Simple training repo for Great Expectations  
```bash
# Create new folder
mkdir tjf_ge_2023-09

# Move to new folder
cd tjf_ge_2023-09

# Clone git repository
git clone https://github.com/coded-by-pascal/training_great_expectations.git

# Create virtual ennvironment and install requirements
python3 -mvenv venv
source venv/bin/activate
python3 -mpip install --upgrade pip
python3 -mpip install -r training_great_expectations/requirements.txt

# Initialize Great Expectations
great_expectations init
```

### Expectation

```bash
# Your folder should look like this
tjf_ge_2023-09
├── gx
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
