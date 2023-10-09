from parseData import loadTestData, printTestData
from optimizer import solve


def main():
    filepath = 'Tests/test4.txt'
    schedule, structures = loadTestData(filepath)
    printTestData(schedule, structures)
    print('Testing file', filepath)
    solve(structures, schedule)
    print('Program completed.')


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
