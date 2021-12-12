import argparse
from cases import case1, case2, case3
from logs import Logs

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', type=int,
                        help="specify case number")
    args = parser.parse_args()
    case_number = args.case
    Logs()
    if case_number == 1:
        case1()
    elif case_number == 2:
        case2()
    elif case_number == 3:
        case3()
    else:
        raise Exception("Invalid case number, available case numbers are 1, 2 and 3")
