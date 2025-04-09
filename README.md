# openLayup

![Alt text](resources/oL-logo.svg)

## Overview

**openLayup** is an open-source, GUI-based structural simulation tool for aerospace structures. The software estimates key mechanical metrics such as stress, strain, and factor of safety based on material properties, ply layup configurations, and component geometries. It applies **Classical Laminate Theory (CLT)** and the **Tsai-Wu failure criterion**, enabling laminate-level failure-mode analysis across various aerospace components.

> _Note: openLayup is inspired by [openMotor](https://github.com/reilleya/openMotor), an open-source internal ballistics simulator for solid rocket motors. It follows a similar philosophy of enabling experimental, iterative workflows for engineers and designers._

---

## Planned Features

- Support for composite and isotropic materials  
- Ply-level configuration, including orientation and stacking sequence  
- Common component geometries: nosecones, airframes, fins  
- Material database with user-editable properties  
- CLT-based analysis of in-plane and out-of-plane behavior  
- Failure mode estimation using the Tsai-Wu criterion  
- Metric and imperial unit support  
- Design visualization and layout overview  
- Save/load project functionality  
- Thermal loading and expansion analysis  
- Buckling prediction for thin-walled structures  
- Finite element mesh export for external analysis tools  
- Additional failure criteria (e.g., Maximum Stress, Hashin)  
- Aero load simulation integration  

---

## Download

To be added. A standalone installer and executable will be provided in future releases. For now, see the instructions below for building from source.

---

## Building from Source

**Requirements**

- Python 3.10 or newer  
- Qt6 (for GUI interface)  

**Dependencies**

- `PyQt6`  
- `numpy`  
- `scipy`  
- `matplotlib`  

**Installation Steps**

```bash
$ git clone https://github.com/your-username/openLayup
$ cd openLayup
$ python3 -m venv .venv
$ source .venv/bin/activate         # On Windows: .venv\Scripts\activate
$ pip install -r requirements.txt
