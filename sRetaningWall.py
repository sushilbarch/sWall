import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFileDialog
import matplotlib.pyplot as plt
import pandas as pd
import ezdxf

class RetainingWallApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Retaining Wall Design')
        layout = QVBoxLayout()

        # Input fields
        self.inputs = {}
        input_labels = [
            ('Channage From:', 'channage_from'),
            ('Channage To:', 'channage_to'),
            ('Depth of Foundation for soling and PCC (m):', 'depth_foundation'),
            ('Width of Foundation (m):', 'width_foundation'),
            ('Top Width of Wall (m):', 'top_width'),
            ('Height of Retaining Wall (m):', 'height_wall'),
            ('Length of Retaining Wall (m):', 'length_wall')
        ]

        for label_text, key in input_labels:
            label = QLabel(label_text)
            input_field = QLineEdit()
            layout.addWidget(label)
            layout.addWidget(input_field)
            self.inputs[key] = input_field

        # Calculate button
        self.calculate_button = QPushButton('Calculate and Draw', self)
        self.calculate_button.clicked.connect(self.calculate_and_draw)
        layout.addWidget(self.calculate_button)

        self.setLayout(layout)

    def calculate_and_draw(self):
        try:
            # Fetching input values
            depth_foundation = float(self.inputs['depth_foundation'].text())
            width_foundation = float(self.inputs['width_foundation'].text())
            top_width = float(self.inputs['top_width'].text())
            height_wall = float(self.inputs['height_wall'].text())
            length_wall = float(self.inputs['length_wall'].text())
            channage_from = self.inputs['channage_from'].text()
            channage_to = self.inputs['channage_to'].text()

            # Constant values
            depth_pcc = 0.1  # Thickness of PCC below foundation (m)
            stone_soling = 0.15  # Stone soling thickness (m)
            base_width = 0.5 * height_wall  # Base width typically 0.5 to 0.7 times the height

            # Calculations
            foundation_earthwork = length_wall * base_width * (depth_foundation + depth_pcc + stone_soling)
            foundation_stone_soling = length_wall * base_width * stone_soling
            foundation_pcc = length_wall * base_width * depth_pcc
            stone_masonry = length_wall * (base_width + top_width) * height_wall / 2
            top_pcc = length_wall * top_width * 0.05  # Assuming a 0.05m thick PCC layer on top

            # Prepare data for Excel
            remarks = f"Channage from {channage_from} to {channage_to}"
            data = [
                [1, 'Foundation Earthwork', 'cu.m', 1, length_wall, base_width, depth_foundation + depth_pcc + stone_soling, foundation_earthwork, remarks],
                [2, 'Foundation Stone Soling', 'cu.m', 1, length_wall, base_width, stone_soling, foundation_stone_soling, remarks],
                [3, 'Foundation PCC', 'cu.m', 1, length_wall, base_width, depth_pcc, foundation_pcc, remarks],
                [4, 'Stone Masonry', 'cu.m', 1, length_wall, (base_width + top_width) / 2, height_wall, stone_masonry, remarks],
                [5, 'Top PCC', 'cu.m', 1, length_wall, top_width, 0.05, top_pcc, remarks]
            ]

            columns = ['S.N', 'Description of Item', 'Unit', 'Number', 'Length (m)', 'Width (m)', 'Height (m)', 'Quantity', 'Remarks']
            df = pd.DataFrame(data, columns=columns)

            # Save to Excel
            options = QFileDialog.Options()
            excel_file_path, _ = QFileDialog.getSaveFileName(self, "Save Excel File", f"retaining_wall_calculations_{channage_from}_to_{channage_to}.xlsx", "Excel Files (*.xlsx)", options=options)
            if excel_file_path:
                df.to_excel(excel_file_path, index=False)

            # Display calculations in a message box
            results = (f"Foundation Earthwork: {foundation_earthwork:.2f} cubic meters\n"
                       f"Foundation Stone Soling: {foundation_stone_soling:.2f} cubic meters\n"
                       f"Foundation PCC: {foundation_pcc:.2f} cubic meters\n"
                       f"Stone Masonry: {stone_masonry:.2f} cubic meters\n"
                       f"Top PCC: {top_pcc:.2f} cubic meters\n")

            QMessageBox.information(self, "Calculation Results", results)

            # Drawing the retaining wall and saving as CAD
            self.draw_retaining_wall(depth_foundation, base_width, depth_pcc, stone_soling, top_width, height_wall, length_wall)
            self.save_cad_file(depth_foundation, base_width, depth_pcc, stone_soling, top_width, height_wall, length_wall, channage_from, channage_to)

        except ValueError:
            QMessageBox.critical(self, "Input Error", "Please enter valid numeric values.")

    def draw_retaining_wall(self, depth_foundation, base_width, depth_pcc, stone_soling, top_width, height_wall, length_wall):
        # Draw front elevation and cross-section using matplotlib

        fig, ax = plt.subplots(1, 2, figsize=(12, 6))

        # Front elevation
        ax[0].set_title("Front Elevation")
        ax[0].plot([0, 0], [0, -depth_foundation], color='black')  # Left vertical line
        ax[0].plot([0, length_wall], [-depth_foundation, -depth_foundation], color='black')  # Bottom line
        ax[0].plot([length_wall, length_wall], [-depth_foundation, height_wall], color='black')  # Right vertical line
        ax[0].plot([length_wall, 0], [height_wall, height_wall], color='black')  # Top line
        ax[0].plot([0, 0], [0, height_wall], color='black')  # Left vertical wall

        # Fill foundation and wall
        ax[0].fill_between([0, length_wall], [-depth_foundation, -depth_foundation], 0, color='gray', alpha=0.5)
        
        # Adding weep holes for drainage at middle level of wall
        ax[0].scatter([length_wall * 0.2, length_wall * 0.8], [height_wall * 0.5, height_wall * 0.5], color='blue')  # Weep holes at middle level

        # Fill top PCC layer
        ax[0].fill_between([0, length_wall], [height_wall, height_wall], height_wall + 0.1, color='brown', alpha=0.5, label='Top PCC')

        ax[0].set_xlim(-0.5, length_wall + 0.5)
        ax[0].set_ylim(-depth_foundation - 1, height_wall + 1)
        ax[0].set_aspect('equal')
        ax[0].set_xlabel("Length (m)")
        ax[0].set_ylabel("Height (m)")

        # Cross-section
        ax[1].set_title("Cross Section")
        ax[1].plot([0, 0], [0, -depth_foundation], color='black')  # Left foundation line
        ax[1].plot([0, base_width], [-depth_foundation, -depth_foundation], color='black')  # Bottom line
        ax[1].plot([base_width, base_width], [-depth_foundation, 0], color='black')  # Right foundation line
        ax[1].plot([base_width, base_width - (base_width - top_width)], [0, height_wall], color='black')  # Wall slant line
        ax[1].plot([base_width - (base_width - top_width), 0], [height_wall, height_wall], color='black')  # Top line
        ax[1].plot([0, 0], [0, height_wall], color='black')  # Left vertical wall

        # Fill layers for cross-section
        ax[1].fill_between([0, base_width], [-depth_foundation, -depth_foundation], color='yellow', alpha=0.5, label='Stone Soling')
        ax[1].fill_between([0, base_width], [-depth_foundation - depth_pcc, -depth_foundation], color='brown', alpha=0.5, label='PCC')

        # Adding weep holes for drainage at middle level of wall
        ax[1].scatter([base_width * 0.1, base_width * 0.4], [height_wall * 0.5, height_wall * 0.5], color='blue')  # Weep holes at middle level

        ax[1].set_xlim(-0.5, base_width + 0.5)
        ax[1].set_ylim(-depth_foundation - 1, height_wall + 1)
        ax[1].set_aspect('equal')
        ax[1].set_xlabel("Width (m)")
        ax[1].set_ylabel("Height (m)")

        plt.tight_layout()
        plt.show()

    def save_cad_file(self, depth_foundation, base_width, depth_pcc, stone_soling, top_width, height_wall, length_wall, channage_from, channage_to):
        # Create a CAD drawing using ezdxf
        doc = ezdxf.new()
        msp = doc.modelspace()

        # Front elevation
        msp.add_line((0, 0), (0, -depth_foundation))  # Left vertical line
        msp.add_line((0, -depth_foundation), (length_wall, -depth_foundation))  # Bottom line
        msp.add_line((length_wall, -depth_foundation), (length_wall, height_wall))  # Right vertical line
        msp.add_line((length_wall, height_wall), (0, height_wall))  # Top line
        msp.add_line((0, height_wall), (0, 0))  # Left vertical wall

        # Cross-section
        msp.add_line((0, 0), (0, -depth_foundation))  # Left foundation line
        msp.add_line((0, -depth_foundation), (base_width, -depth_foundation))  # Bottom line
        msp.add_line((base_width, -depth_foundation), (base_width, 0))  # Right foundation line
        msp.add_line((base_width, 0), (base_width - (base_width - top_width), height_wall))  # Wall slant line
        msp.add_line((base_width - (base_width - top_width), height_wall), (0, height_wall))  # Top line
        msp.add_line((0, height_wall), (0, 0))  # Left vertical wall

        # Save CAD file
        options = QFileDialog.Options()
        cad_file_path, _ = QFileDialog.getSaveFileName(self, "Save CAD File", f"retaining_wall_drawing_{channage_from}_to_{channage_to}.dxf", "DXF Files (*.dxf)", options=options)
        if cad_file_path:
            doc.saveas(cad_file_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RetainingWallApp()
    ex.show()
    sys.exit(app.exec_())
