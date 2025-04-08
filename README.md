#openLayup

##Overview
openLayup is an open-source, GUI-based structural simulation tool for aerospace structures. The software estimates mechanical metrics such as stress, strain, and factor of safety based on material properties, ply layup configurations, and component geometries. It uses Classical Laminate Theory (CLT) and the Tsai-Wu failure criterion to support structural failure-mode analysis.

Note: This project is inspired by openMotor, an open-source internal ballistics simulator for solid rocket motors. openLayup follows a similar design philosophy to assist experimenters and engineers in iterative design and analysis workflows.

Planned Features
*Support for composite and isotropic materials
*Ply-level configuration, including orientation and stacking sequence
*Common component geometries: nosecones, airframes, fins
*Material database with user-editable properties
*CLT-based analysis of in-plane and out-of-plane behavior
*Failure mode estimation using the Tsai-Wu criterion
*Metric and imperial units
*Design visualization and layout overview
*Save/load project functionality
*Thermal loading and expansion analysis
*Buckling prediction for thin-walled structures
*Finite element mesh export for external analysis tools
*More failure criteria (e.g. Maximum Stress, Hashin)
*Aero load simulation integration

##Download
[...]

##Building from Source
Requirements:
Python 3.10 or newer
Qt6 (required for GUI)

Dependencies: PyQt6, numpy, scipy, matplotlib

Installation Steps
bash
Copy
Edit
$ git clone https://github.com/your-username/openLayup
$ cd openLayup
$ python3 -m venv .venv
$ source .venv/bin/activate         # Use `.venv\Scripts\activate` on Windows
$ pip install -r requirements.txt
If you encounter errors during installation, ensure that your system has the appropriate development headers:

##Data Files
openLayup uses YAML for storing user data and project files. Project files are saved with the [..] extension and can be opened or edited in a standard text editor.


##License
openLayup is released under the GNU General Public License v3. The source code is provided to ensure transparency, reproducibility, and community-driven development.

##Contributing
Contributions are welcome. If you encounter a bug or have a feature suggestion, please open an issue. Pull requests with new features, UI improvements, or performance enhancements are encouraged.

To contribute:
*Fork the repository
*Create a feature branch
*Submit a pull request with a clear description
