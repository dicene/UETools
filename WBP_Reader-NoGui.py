import json
import typing

Name: str = "N/A"
Generated_Class = None
CDO = None
SuperStruct = None
Functions = []
Properties = []

with open('WBPSample.json', 'r') as file:
    data = json.load(file)
    print(f"Sample data: {len(data)}")
    for item in data:
        if item['Flags'].find('RF_ClassDefaultObject') >= 0:
            CDO = item
            print(f"CDO: {item['Name']}")
        elif item['Type'] == "WidgetBlueprintGeneratedClass":
            Generated_Class = item
            Name = item['Name']
            print(f"WidgetBlueprintGeneratedClass: {Name}")
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
