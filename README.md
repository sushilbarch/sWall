# sWall
Sample wall desing drawing and quantity calculation in Nepal in local level.
The provided code is a Python program that uses PyQt5 to create a GUI application for retaining wall design. The application calculates quantities, generates drawings, and allows users to save data in Excel and CAD formats. Here's a detailed description:

1. Overview
The program uses PyQt5 to create a graphical user interface.
It allows users to input retaining wall parameters, calculates the quantities, and provides visual representations of the retaining wall in the form of a front elevation and a cross-section.
The application also has the functionality to save the output as an Excel file or a CAD drawing in DXF format.
2. Libraries Used
sys: To handle command-line arguments and application exit.
PyQt5.QtWidgets: Provides widgets for the user interface like QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, etc.
matplotlib.pyplot: To plot the front elevation and cross-section of the retaining wall.
pandas: To create and export calculated data to Excel files.
ezdxf: To create a CAD file of the retaining wall drawing in DXF format.
3. GUI Components
3.1 RetainingWallApp Class
The RetainingWallApp class is a QWidget-based class that creates a user interface for the retaining wall design.

Initialization (__init__):

The class is initialized using super().__init__().
The init_ui() method is called to set up the UI.
User Interface (init_ui()):

The window is titled 'Retaining Wall Design'.
Uses QVBoxLayout to arrange input fields vertically.
A dictionary (self.inputs) is used to store input fields for easy access.
Input Fields:

Several QLabel and QLineEdit elements are used to take inputs such as:
Channage From and Channage To: To indicate the section being worked on.
Depth of Foundation, Width of Foundation, Top Width, Height of Retaining Wall, and Length of Retaining Wall.
Calculate Button:

A Calculate and Draw button is provided to initiate the calculations and drawing.
The calculate_and_draw() method is called when the button is clicked.
4. Core Functionalities
4.1 Calculations and Drawing (calculate_and_draw()):
Input Fetching and Conversion:

Retrieves user input values from the input fields and converts them to float.
Constant Values:

Some default values are defined for calculations:
Depth of PCC = 0.1 m
Stone Soling Thickness = 0.15 m
Base Width = 0.5 * height of the wall (assumed to be 50% of the wall height)
Quantity Calculations:

Calculates quantities for:
Foundation Earthwork
Foundation Stone Soling
Foundation PCC
Stone Masonry
Top PCC (assumed to be 0.05m thick)
Excel Export:

The calculated values are saved into an Excel sheet using pandas.
QFileDialog is used to ask the user where to save the file.
The data frame is constructed with columns such as S.N, Description of Item, Unit, Number, Length (m), Width (m), Height (m), Quantity, and Remarks.
Results Display:

Displays the calculated values in a QMessageBox for easy reference.
Drawing:

Calls draw_retaining_wall() to create graphical representations of the retaining wall.
4.2 Drawing the Retaining Wall (draw_retaining_wall()):
Front Elevation and Cross-Section:
Uses Matplotlib to create a front elevation and a cross-section.
Front Elevation:
Draws the left vertical wall, foundation, and top lines.
Fills areas such as the foundation and top PCC using colors for visual clarity.
Adds weep holes (shown as blue dots) for drainage purposes.
Cross-Section:
Draws the foundation, stone soling, and PCC.
Again, weep holes are added to demonstrate proper drainage.
Plotting:
fig, ax = plt.subplots(1, 2) is used to create two subplots: one for the front elevation and one for the cross-section.
Uses functions like plot() and fill_between() to draw lines and fill areas.
4.3 Save CAD Drawing (save_cad_file()):
CAD File Generation Using EzDXF:
Creates a new DXF drawing using ezdxf.new().
Adds lines to the drawing for the front elevation and cross-section.
QFileDialog is used to prompt the user for the file path to save the CAD file.
The drawing includes:
Foundation, retaining wall, and top PCC lines.
5. Flow of the Program
User Opens Application:
Launches the retaining wall design application.
Inputs Values:
User inputs parameters like channage, depth, widths, height, etc.
Click Calculate and Draw:
The button triggers calculations, displays results, and creates drawings.
Outputs:
Excel File: User can save the calculated quantities as an Excel file.
CAD File: The application generates a CAD drawing of the retaining wall.
6. Key Features
User Input Handling:
All user inputs are converted to floats for calculations, and errors are handled using QMessageBox.
Calculations:
The application calculates the required quantities for different elements like foundation, stone masonry, and PCC.
Graphical Drawing:
Matplotlib is used for visualizing the retaining wall's front elevation and cross-section.
CAD Output:
The program allows saving a CAD representation of the wall as a DXF file using EzDXF.
Excel Export:
Quantities are exported to Excel using Pandas, allowing easy sharing and further analysis.
7. Improvements and Extensions
Input Validation:
Add specific validation for different input fields to prevent incorrect entries.
Add More Options:
Allow the user to adjust more design parameters, such as slope or base width ratio.
User Experience:
The UI could be enhanced using styling and providing tooltips for each input field.
Reinforcement Calculation:
Add reinforcement details for structural stability analysis.
8. Summary
This program is a basic yet functional GUI application for the design of retaining walls. It takes user inputs, calculates quantities for different construction elements, draws visual representations, and generates output files in Excel and CAD formats. It is well-suited for civil engineers who want an intuitive interface for retaining wall design and quantity estimation.

The core benefits of this program include:

Simplified data entry.
Instant calculations of construction quantities.
Visual representation of the retaining wall.
CAD and Excel file output for further use.
