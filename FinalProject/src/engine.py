import argparse
import os
import time
from analysis import *



#get_args() which uses the argparse library to parse command line arguments.
#It then checks the validity of the provided files and directories, and if they are valid it starts the analysis process.
#It prints some information about the provided arguments, and calls the main_func() function to audit the spec file.
#It then calls the engine binary with the audited spec file and input files as arguments.
#It then calls a python script to open a GUI to display the results.




def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--spec', dest='spec', default=None,
                        type=str, help='The location of the full spec file')
    parser.add_argument('--specDefine', dest='specDefine', default=None,
                        type=str, help='The location of the define files for spec file')
    parser.add_argument('--input', dest='input', default=None,
                        type=str, help='The location of input files')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    spec = args.spec
    target = args.input
    specDefine = args.specDefine
    if spec is None:
        print("Please provide spec file by --spec=Path2Spec")
        exit(1)
    if not os.path.isfile(spec):
        print("Could not find spec file! " + spec)
        exit(1)
    if (not specDefine) and (not os.path.isfile(specDefine)):
        print("Could not find specDefine file! " + specDefine)
        exit(1)
    if target is None:
        print("Please provide target analysis file by --input=Path2Input")
        exit(1)
    if not os.path.isfile(target):
        print("Could not find input file! " + target)
        exit(1)
    if not str(target).endswith("c"):
        print("Currently we only accept *.c files as input")
    print("User Input =>")
    print("Spec Location: {}\nInput Location: {}".format(spec, target))
    specPath = os.path.abspath(spec)
    specDefinePath = os.path.abspath(specDefine)
    targetPath = os.path.abspath(target)
    print("auditing spec file =>")
    audit = main_func(specPath, specDefinePath)
    auditPath = os.path.join(os.path.dirname(specPath), audit)
    resultPath = os.path.join(os.path.dirname(specPath), "logResult.yaml")
    # print(auditPath)

    
    cmdStr = "cd engine; bin/engine --config config/bugdetector.top --spec {} {}".format(auditPath, targetPath)
    print(cmdStr)
    os.system(cmdStr)
    print("The checking result in {}".format(resultPath))
    cmdStr = "python3 report_displayerGUI.py"
    print("Using report_displayerGUI to validate the result:\nOpening Report Displayer GUI...")
    time.sleep(3)
    os.system(cmdStr)
