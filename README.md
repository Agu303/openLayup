openLayup
openLayup is an open-source, GUI-based structural simulation tool for aerospace structures. The software estimates mechanical metrics such as stress, strain, and factor of safety based on material properties, ply layup configurations, and component geometries. It uses Classical Laminate Theory (CLT) and the Tsai-Wu failure criterion to support structural failure-mode analysis.

Note: This project is inspired by openMotor, an open-source internal ballistics simulator for solid rocket motors. openLayup follows a similar design philosophy to assist experimenters and engineers in iterative design and analysis workflows.

Features
Support for composite and isotropic materials

Ply-level configuration, including orientation and stacking sequence

Common component geometries: nosecones, airframes, fins

Material database with user-editable properties

CLT-based analysis of in-plane and out-of-plane behavior

Failure mode estimation using the Tsai-Wu criterion

Metric and imperial units

Design visualization and layout overview

Save/load project functionality

Planned Features
Thermal loading and expansion analysis

Buckling prediction for thin-walled structures

Finite element mesh export for external analysis tools

More failure criteria (e.g. Maximum Stress, Hashin)

Aero load simulation integration

Download
The latest release is available here. Download and unzip the package for your system and run the executable to get started. Alternatively, follow the instructions below to run from source for the most up-to-date features.

Building from Source
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

For example:

bash
Copy
Edit
# On Debian/Ubuntu
$ sudo apt install python3-dev
UI Files
The UI is designed using Qt Designer and stored as .ui files. These must be converted into Python code using pyuic6:

bash
Copy
Edit
$ python setup.py build_ui
If you make changes to the GUI, re-run the command above to regenerate the Python bindings.

Running the Application
Once the environment is set up and UI files are built:

bash
Copy
Edit
$ python main.py
Data Files
openLayup uses YAML for storing user data and project files. Project files are saved with the .layup extension and can be opened or edited in a standard text editor.

Application data is saved in the following locations depending on the platform:

Windows: %AppData%\openLayup

macOS: ~/Library/Application Support/openLayup

Linux: ~/.local/share/openLayup

License
openLayup is released under the GNU General Public License v3. The source code is provided to ensure transparency, reproducibility, and community-driven development.

Contributing
Contributions are welcome. If you encounter a bug or have a feature suggestion, please open an issue. Pull requests with new features, UI improvements, or performance enhancements are encouraged.

To contribute:

Fork the repository

Create a feature branch

Submit a pull request with a clear description
