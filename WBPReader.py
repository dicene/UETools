import json

with open('WBPSample.json', 'r') as file:
    data = json.load(file)
    print(f"Sample data: {len(data)}")
    for item in data:
        if item['Type'] == 'Function':
            print(f"Function: {item['Class']}: {item['Name']}")
            if 'SuperStruct' in item:
                #print(f"Function: {item['Class']}: {item['Name']}")
                print(f"\tSuperStruct: {item['SuperStruct']['ObjectName']}")
                pass
            elif 'ChildProperties' in item:
                for childProperty in item['ChildProperties']:
                    if childProperty['Name'].endswith('ReturnValue'):
                        if childProperty['Type'] == "StructProperty" and 'Struct' in childProperty:
                            print(f"\tStruct: {childProperty['Struct']}")

                        print(f"\tReturn property: {childProperty['Name']}")
            else:
                print("No child properties or superStruct?")
        else:
            print(f"   Field:    {item['Type']}: {item['Name']}")
