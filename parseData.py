from classDefinitions import *


def parse_vacations(line):
    parts = line.split(': ')
    worker_id = int(parts[0])
    vacation_data = parts[1].split()
    vacations = []
    for vacation in vacation_data:
        vacation = vacation.split('.')
        if vacation[1] == '0':
            vacation = Vacation(vacation[0], True)
        else:
            vacation = Vacation(vacation[0], False)
        vacations.append(vacation)
    return worker_id, vacations


def parse_structure(line):
    parts = line.split(': ')
    struct_id = int(parts[0])
    full_time = []
    half_time = []
    if parts[1][0] != "\\" and parts[1][-1] != "\\":
        workers_data = parts[1].split(' \\ ')
        full_time = [int(id_str) for id_str in workers_data[0].split()]
        half_time = [int(id_str) for id_str in workers_data[1].split()]
    elif parts[1][0] != "\\":  # there are only full-time workers
        full_time = [int(id_str) for id_str in parts[1].replace(" \\", '').split()]
    elif parts[1][-1] != "\\":  # there are half-time workers
        half_time = [int(id_str) for id_str in parts[1].replace("\\ ", '').split()]
    workers = []
    for i in range(len(full_time)):
        worker = Worker(full_time[i], True, [])
        workers.append(worker)
    for i in range(len(half_time)):
        worker = Worker(half_time[i], False, [])
        workers.append(worker)
    structure = Structure(struct_id, workers)
    return structure


def parse_schedule(line):
    spaceNum, dayNum = map(int, line.split(' \\ '))
    return Schedule(spaceNum, dayNum)


def loadTestData(filename):
    # Read the data from the text file
    with open(filename, 'r') as file:
        lines = file.read().splitlines()

    # Initialize variables to store parsed data
    structures = []
    current_structure = None
    separators_count = 0

    # Create Schedule variable
    schedule = parse_schedule(lines[0])

    # Iterate through the lines in the file
    for line in lines[1:]:
        if line.startswith("--"):
            separators_count += 1
            continue  # Skip the separator line
        elif separators_count == 1:  # Parse line into Structure
            structures.append(parse_structure(line))
            continue
        elif separators_count == 2:  # Parse line into Structure.workers[x].vacations
            work_id, vacations = parse_vacations(line)
            if vacations:
                for structure in structures:
                    for worker in structure.workers:
                        if worker.work_id == work_id:
                            for vacation in vacations:
                                worker.vacations.append(vacation)
            continue

    if current_structure:
        structures.append(current_structure)

    return schedule, structures


def printTestData(schedule, structures):
    print(f"Schedule for {schedule.dayNum} days in a workspace with {schedule.spaceNum} desks")
    print("Business data:")
    print(f"{len(structures)} total structures")
    for structure in structures:
        print(f"Structure {structure.struct_id}:")
        for worker in structure.workers:
            if worker.isFullTime:
                print(f"\tWorker {worker.work_id} (full-time)")
            else:
                print(f"\tWorker {worker.work_id} (half-time)")
            if worker.vacations:
                print("\tVacations:")
                for vacation in worker.vacations:
                    if vacation.isMorning:
                        print(f"\t\tDay {vacation.day}, morning")
                    else:
                        print(f"\t\tDay {vacation.day}, afternoon")
            print()
        print("---------------------------------")
