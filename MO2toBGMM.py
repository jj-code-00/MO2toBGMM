from pathlib import Path
import json


def get_paths():
    profile_path = input("Enter absolute path to your mo2 profile, Ex. C:\\\\Listonomicon\\\\profiles\\\\Listonomicon\n")
    mod_settings_path = profile_path + "\\modsettings.lsx"
    return Path(mod_settings_path).read_text()


def read_file(textdata):
    read_this = 0

    output = {
        "Order": []
    }

    chunk = {
        "UUID": "",
        "Name": ""}

    for line in textdata.splitlines():

        if line.startswith("            <node id=\"ModuleShortDesc\">"):
            read_this = 1

        if line.startswith("              <attribute id=\"UUID\" value=\"") & read_this == 1:
            line1 = line.split("              <attribute id=\"UUID\" value=\"", 1)
            line2 = line1[1].split("\" type=\"FixedString\"/>")
            if line2[0] != "28ac9ce2-2aba-8cda-b3b5-6e922f71b6b8":
                chunk["UUID"] = line2[0]
                output["Order"].append(chunk)
                chunk = {
                    "UUID": "",
                    "Name": ""}
            read_this = 0

        if line.startswith("              <attribute id=\"Name\" value=\"") & read_this == 1:
            line1 = line.split("              <attribute id=\"Name\" value=\"", 1)
            line2 = line1[1].split("\" type=\"FixedString\"/>")
            line3 = line2[0].split("\" type=\"LSString\"/>")
            if line3[0] != "GustavDev":
                chunk["Name"] = line3[0]
    return output


if __name__ == '__main__':
    file = read_file(get_paths())

    with open("LoadOrder.json", "w") as write_file:
        json.dump(file, write_file, indent=2)