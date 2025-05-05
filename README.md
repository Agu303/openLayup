# openLayup

![Alt text](resources/oL-logo.svg)

## Overview

**openLayup** is an open-source, GUI-based structural simulation tool for rocketry structural components. The software estimates key mechanical metrics such as stress, strain, and factor of safety based on material properties, ply layup configurations, and component geometries. It applies multiple failure methods, enabling laminate-level failure-mode analysis across various aerostructural components.  This is aimed to be a specialized tool bridging the gap between simplified analysis and full-scale FEA for composite rocket structures. 

> _Note: openLayup is inspired by [openMotor](https://github.com/reilleya/openMotor), an open-source internal ballistics simulator for solid rocket motors. It follows a similar philosophy of enabling experimental, iterative workflows for engineers and designers._

---

## Planned Features

- Support for composite and isotropic materials  
- Ply-level configuration, including orientation and stacking sequence  
- Common component geometries presets: nosecones, airframes, fins  
- Material database with user-editable properties  
- CLT-based analysis of in-plane and out-of-plane behavior  
- Failure mode analysis using **Max Stress/Strain criteria, CLT, Tsai-Wu, Tsai-Hill, Hashin-Rotem, and Puck Criterion**
- Save/load project functionality  
- Buckling prediction for thin-walled structures
- Integrate efficiently with openRocket, SolidWorks, and ANSYS workflow
*Thermal loading and expansion analysis
*Design visualization and layout overview
*Metric and imperial unit support  


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
$ git clone https://github.com/Agu303/openLayup.git
$ cd openLayup
$ uv run main.py
```
c w/h