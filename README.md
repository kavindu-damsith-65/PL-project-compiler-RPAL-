<div align="center">

# RPAL Interpreter

**A complete language-processing path from RPAL source to CSE-machine evaluation.**

<img src="https://img.shields.io/badge/Completed_academic_compiler_project-4F86FF?style=flat-square&labelColor=0B1224" alt="Completed academic compiler project" /> <img src="https://img.shields.io/badge/Public_repository-4F86FF?style=flat-square&labelColor=0B1224" alt="Public repository" />

[Portfolio](https://kavindudamsith.tech/) &nbsp;|&nbsp; [LinkedIn](https://www.linkedin.com/in/kavindu-damsith-86696722a/) &nbsp;|&nbsp; [Email](mailto:kavindudamsith65@gmail.com)

</div>

---

## Overview

This academic compiler project implements lexical processing, parsing, abstract syntax tree creation, standardisation, environments, primitive operations, and execution on a CSE machine. The repository also contains the original project specification and RPAL test programs.

## What it does

| Area | Details |
| --- | --- |
| **Front end** | Tokenisation and recursive parsing build the abstract syntax tree. |
| **Standardisation** | Language constructs are transformed into a standard tree form. |
| **Runtime model** | Environments, values, tuples, and operation handlers model program state. |
| **Evaluation** | The CSE machine executes the standardised representation. |

## Repository map

| Path | Purpose |
| --- | --- |
| `reCreate/main/lexicon.py and parser1.py` | Lexical analysis and parser. |
| `reCreate/main/AST/` | Abstract syntax tree representation. |
| `reCreate/main/INTERPRETER/` | Standardisation and operation handling. |
| `reCreate/main/CSE/` | CSE machine, environments, and runtime elements. |
| `reCreate/rpal/` | Reference programs and test inputs. |

## Technology

- **Python**
- **Parsing**
- **AST**
- **CSE Machine**

## Local setup

```bash
cd reCreate/main
python main.py ../rpal/fn1
```

### Configuration notes

The included Makefile and reference files reflect the university project environment. Run from the implementation directory so relative test paths resolve correctly.

## Status

Completed academic compiler project.

## Links

- [Portfolio project index](https://kavindudamsith.tech/#work)

---

Questions about this repository? [Email me](mailto:kavindudamsith65@gmail.com) or connect on [LinkedIn](https://www.linkedin.com/in/kavindu-damsith-86696722a/).
