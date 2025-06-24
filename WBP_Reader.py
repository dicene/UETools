import sys
import json
import typing
from PyQt6 import QtWidgets, QtCore, QtGui

Name: str = "N/A"
Generated_Class = None
CDO = None
SuperStruct = None
Functions = []
Properties = []

class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QtWidgets.QVBoxLayout(self)
        # self.count = 0
        # self.button = QtWidgets.QPushButton(f"Click Count: {self.count}", self)
        # self.button.setFixedSize(120, 60)
        # self.button.clicked.connect(self.count_clicks)
        # layout = QtWidgets.QVBoxLayout()
        # layout.addWidget(self.button)
        self.timer = QtCore.QTimer(self)
        # self.timer.timeout.connect(self.tick)
        # self.timer.start(100)

        self.path_block = QtWidgets.QHBoxLayout(self)
        self.path_label = QtWidgets.QLabel(self)
        self.path_label.setText("Asset Path:")
        self.path_block.addWidget(self.path_label)
        self.path_edit = QtWidgets.QLineEdit(self)
        self.path_block.addWidget(self.path_edit)
        self.path_button = QtWidgets.QPushButton(self)
        self.path_button.setText("Browse")
        self.path_button.clicked.connect(self.select_wbp_file)
        self.path_block.addWidget(self.path_button)
        layout.addLayout(self.path_block)

        self.name_block = QtWidgets.QHBoxLayout(self)
        self.name_label = QtWidgets.QLabel(self)
        self.name_label.setText("Name: ")
        self.name_block.addWidget(self.name_label)
        self.name_edit = QtWidgets.QLineEdit(self)
        self.name_block.addWidget(self.name_edit)
        layout.addLayout(self.name_block)

        self.cdo_block = QtWidgets.QHBoxLayout(self)
        self.cdo_label = QtWidgets.QLabel(self)
        self.cdo_label.setText("CDO: ")
        self.cdo_block.addWidget(self.cdo_label)
        self.cdo_edit = QtWidgets.QLineEdit(self)
        self.cdo_block.addWidget(self.cdo_edit)
        layout.addLayout(self.cdo_block)
        self.cdo_text = QtWidgets.QLabel(self)
        layout.addWidget(self.cdo_text)

        self.function_list_label = QtWidgets.QLabel(self)
        self.function_list_label.setText("Functions:")
        layout.addWidget(self.function_list_label)
        self.function_list = QtWidgets.QListWidget(self)
        layout.addWidget(self.function_list)

        self.bp_tree = QtWidgets.QTreeWidget(self)
        # self.bp_tree.setColumnCount(2)
        # self.bp_tree.setHeaderLabels(["abc", "def"])
        # self.bp_tree.sizePolicy().setVerticalPolicy(QtWidgets.QSizePolicy.Policy.Expanding)
        # self.bp_tree.sizePolicy().setVerticalStretch(2)
        layout.addWidget(self.bp_tree)

        # tree.addTopLevelItem(QtWidgets.QTreeWidgetItem(self, "Abc"))
        # layout.addWidget(self.bp_tree)
        # button = QtWidgets.QPushButton(self)
        # button.setText("ABC")
        # button.setFixedSize(300, 100)
        # layout.addWidget(button)

        self.setLayout(layout)
        self.load_settings()
        self.load_blueprint()

    def select_wbp_file(self):
        self.file_selector = QtWidgets.QFileDialog(self)
        self.file_selector.fileSelected.connect(self.file_selected)
        results = self.file_selector.getOpenFileName(self, "Select a WBP json file")
        self.path_edit.setText(results[0])
        self.settings.setValue("WBP_Path", results[0])
        # print(f"Selected file: {results} {self.file_selector.fileSelected}")
        # self.file_selector.selectFile("New WBP Reader")
        # self.file_selector.exec()
        # self.file_selector.fileSelected.connect()

    def file_selected(self):
        print(f"File selected!")

    def load_settings(self):
        self.settings = QtCore.QSettings('Di', 'WBP_Reader')
        self.path_edit.setText(self.settings.value("WBP_Path", ""))

    def load_blueprint(self):
        with open(self.path_edit.text(), 'r') as file:
            data = json.load(file)
            print(f"Sample data: {len(data)}")
            for item in data:
                if item['Flags'].find('RF_ClassDefaultObject') >= 0:
                    CDO = item
                    self.cdo_edit.setText(CDO['Name'])
                    print(f"CDO: {item['Name']}")
                elif item['Type'] == "WidgetBlueprintGeneratedClass":
                    Generated_Class = item
                    name = item['Name']
                    self.name_edit.setText(name)
                    print(f"WidgetBlueprintGeneratedClass: {name}")
            if 'SuperStruct' in Generated_Class:
                SuperStruct = Generated_Class['SuperStruct']
                print(f"SuperStruct: {SuperStruct['ObjectName']} ({SuperStruct['ObjectPath']})")
            # if 'Children' in Generated_Class:
            #     print(f"Functions:")
            #     for child in Generated_Class['Children']:
            #         func_name = child['ObjectName'].removeprefix("Function'").removesuffix("'")
            #         Functions.append(func_name)
            #         print(f"\t{func_name}")
            if 'FuncMap' in Generated_Class:
                print("Functions:")
                for func in Generated_Class['FuncMap']:
                    Functions.append(func)
                    newItem = QtWidgets.QListWidgetItem(self.function_list)
                    newItem.setText(func)
                    self.function_list.addItem(newItem)
                    print(f"\t{func}")
            if 'ChildProperties' in Generated_Class:
                print(f"Properties:")
                for child in Generated_Class['ChildProperties']:
                    if child['Type'] == 'StructProperty':
                        className = child['Struct']['ObjectName'].removeprefix("Class'").removesuffix("'")
                        public = child['Flags'].find('RF_Public') >= 0
                        print(f"\t{'public ' if public else ''}{className} {child['Name']}")
                    elif child['Type'] == 'ObjectProperty':
                        className = child['PropertyClass']['ObjectName'].removeprefix("WidgetBlueprintGeneratedClass'").removeprefix("Class'").removesuffix("'")
                        public = child['Flags'].find('RF_Public') >= 0
                        print(f"\t{'public ' if public else ''}{className} {child['Name']}")
                    else:
                        print(f"\tUnknown {child['Type']} {child['Name']}")

            # for item in data:
            #     if item['Type'] == 'Function':
            #         print(f"Function: {item['Class']}: {item['Name']}")
            #         if 'SuperStruct' in item:
            #             #print(f"Function: {item['Class']}: {item['Name']}")
            #             print(f"\tSuperStruct: {item['SuperStruct']['ObjectName']}")
            #             pass
            #         elif 'ChildProperties' in item:
            #             for childProperty in item['ChildProperties']:
            #                 if childProperty['Name'].endswith('ReturnValue'):
            #                     if childProperty['Type'] == "StructProperty" and 'Struct' in childProperty:
            #                         print(f"\tStruct: {childProperty['Struct']}")
            #
            #                     print(f"\tReturn property: {childProperty['Name']}")
            #         else:
            #             print("No child properties or superStruct?")
            #     else:
            #         print(f"   Field:    {item['Type']}: {item['Name']}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('fusion')
    window = Window()
    window.resize(500, 700)
    window.show()

    app.exec()