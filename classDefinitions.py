class Vacation:
    """
    Vacation data for an employee.

    day: on which day the employee is on vacation
    isMorning: is the employee on vacation for the morning shift or evening
    """
    day: int
    isMorning: bool  # True - morning half ; False - evening half

    def __init__(self, day, isMorning):
        self.day = day
        self.isMorning = isMorning


class Worker:
    """
    Employee in a workplace.

    work_id: unique identification number
    isFullTime: is the employee a full-time or half-time employee
    """
    work_id: int
    isFullTime: bool  # True - full-time ; False - half-time
    vacations: list[Vacation]
    hoursWorked: int

    def __init__(self, work_id, isFullTime, vacations):
        self.work_id = work_id
        self.isFullTime = isFullTime
        self.vacations = vacations
        self.hoursWorked = 0


class Structure:
    """
    Business structure of a workplace.

    struct_id: ID number of the Structure
    workers: list of all employees in the structure
    """
    struct_id: int
    workers: list[Worker]

    def __init__(self, struct_id, workers):
        self.struct_id = struct_id
        self.workers = workers


class Schedule:
    """
    Schedule for dynamic workspace.

    spaceNum: how many desks are available in the workspace
    dayNum: for how many days is the schedule calculated
    shiftSchedule: best solution
    evaluation: best solution's evaluation
    """
    spaceNum: int
    dayNum: int
    shiftSchedule: list
    evaluation: float
    localOptimums: list

    def __init__(self, spaceNum, dayNum):
        self.spaceNum = spaceNum
        self.dayNum = dayNum
        self.shiftSchedule = []
        self.evaluation = 0.00000000000000
