# File Integrity Monitoring

A simple File Integrity Monitoring (FIM) tool written in Python.

This project monitors files in a directory by calculating their hash values and detecting changes, new files, and deleted files.

## Features

* File hash calculation
* Support for multiple hash algorithms
* Detect modified files
* Detect new files
* Detect deleted files
* Detect file size changes
* Detect modification time changes
* Store hash values in JSON
* Logging changes to a log file

## Supported Hash Algorithms

* MD5
* SHA1
* SHA224
* SHA256
* SHA384
* SHA512

## Requirements

* Python 3.8 or higher

This project only uses Python standard libraries.

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/file-integrity-monitoring.git
cd file-integrity-monitoring
```

No external Python packages are required.

## Usage

### Initialize

Create the initial hash database:

```bash
python fim.py -i sha256
```

You can also use another supported algorithm:

```bash
python fim.py -i md5
```

### Check

Check files for changes:

```bash
python fim.py -c sha256
```

The algorithm must match the algorithm stored in `hash.json`.

You can also run:

```bash
python fim.py -c
```

In this case, the program uses the algorithm stored in `hash.json`.

### Update

Update the stored hashes:

```bash
python fim.py -u sha256
```

You can also use another algorithm:

```bash
python fim.py -u md5
```

## Example

Initialize the FIM using SHA256:

```bash
python fim.py -i sha256
```

Modify a file and then run:

```bash
python fim.py -c sha256
```

The program will report changes such as:

```text
Content changed: example.txt
Size changed: example.txt
Modification time changed: example.txt
```

## Project Structure

```text
file-integrity-monitoring/
│
├── fim.py
├── README.md
├── .gitignore
└── LICENSE
```

## Disclaimer

This project was created for learning purposes and can be improved with additional features.

## Author

Mohammad Ahmadi Bonakdar
