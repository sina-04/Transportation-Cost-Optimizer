# Transportation Cost Optimizer

A Python command-line solver for constructing initial feasible solutions to
balanced transportation problems with:

- the North-West Corner method;
- Vogel's Approximation Method;
- Russell's Approximation Method.

## Fork and authorship

This repository is a fork of
[`wilhelmcs/transportation-cost`](https://github.com/wilhelmcs/transportation-cost).
The upstream project credits Wilhelm Carstens (`@wolam`); this fork also
records Sina Rezaei (`@sina-04`) in its authorship metadata.

The upstream repository does not publish a software license. Consequently,
this fork does **not** add a new license or grant permission to copy, modify,
or redistribute the upstream implementation. Contact the upstream author
before reusing the code beyond what applicable law permits.

## Setup

```bash
git clone https://github.com/sina-04/Transportation-Cost-Optimizer.git
cd Transportation-Cost-Optimizer
python -m venv .venv
```

Activate the environment and install dependencies:

```bash
# Linux/macOS
source .venv/bin/activate

# Windows PowerShell
.\.venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt
```

## Run

```bash
python transport.py METHOD INPUT_FILE
```

`METHOD` is:

| Value | Approximation method |
| --- | --- |
| `1` | North-West Corner |
| `2` | Vogel |
| `3` | Russell |

Example:

```bash
python transport.py 2 res/problem1.txt
```

An input file contains a supply row, a demand row, and the transportation-cost
matrix as comma-separated values:

```text
2000,2500
1500,2000,1000
8,6,10
10,4,9
```

## Limitations

The methods construct initial transportation solutions; they do not by
themselves prove global optimality. Validate dimensions, balance, and results
before using an output in operational decisions.

## License

No license has been supplied by the upstream project, so none is asserted
here. The absence of a license means normal copyright restrictions apply.
