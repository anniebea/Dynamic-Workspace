import math
import random
import time
import statistics
from queue import Queue

from classDefinitions import *
import numpy as np


def initializeSchedule(schedule, structures):
    """
    Fills each shift with the first full-time worker from a structure.

    :param schedule: empty schedule of correct size
    :param structures: all data about stuctures
    :return: the updated schedule
    """
    for i, day in enumerate(schedule):
        for j, shift in enumerate(day):
            for k, desk in enumerate(shift):
                struct = (i * 2 + j) % len(structures)
                worker = k % len(structures[struct].workers)
                schedule[i][j][k] = structures[struct].workers[worker].work_id
            if len(schedule[i][j]) != len(np.unique(schedule[i][j])):  # remove duplicate workers
                toAdd = len(schedule[i][j]) - len(np.unique(schedule[i][j]))
                schedule[i][j] = np.append(np.unique(schedule[i][j]), np.zeros(toAdd))

            for desk in shift:
                for struct in structures:
                    for worker in struct.workers:
                        if worker.work_id == desk:
                            worker.hoursWorked += 1

    return schedule


def recalculateHours(schedule, structures):
    for struct in structures:
        for worker in struct.workers:
            worker.hoursWorked = 0
            for day in schedule:
                for shift in day:
                    for desk in shift:
                        if int(worker.work_id) == int(desk):
                            worker.hoursWorked += 1
    return structures


def evaluateOvertime(scheduleObj, structures):
    """
    Evaluate how many employees are working an appropriate amount of hours.

    :param scheduleObj: The object containing data about schedule
    :param structures: workplace data
    :return: percentage of non-overworked employees
    """
    otCount = 0
    totalCount = 0

    structures = recalculateHours(scheduleObj.shiftSchedule, structures)

    for struct in structures:
        for worker in struct.workers:
            totalCount += 1
            if worker.isFullTime:
                if worker.hoursWorked > scheduleObj.dayNum * 2:
                    otCount += 1
            else:
                if worker.hoursWorked > scheduleObj.dayNum:
                    otCount += 1

    return (totalCount - otCount) / totalCount  # how many are NOT overworked


def evaluateVacations(schedule, totalTimeSlots, structures):
    """
    Evaluate how many vacations have been taken into account.

    :param schedule: schedule to be evaluated
    :param totalTimeSlots: total amount of timeslots in schedule
    :param structures: workplace data
    :return: percentage of valid timeslots
    """
    invalidTimeSlots = 0
    for struct in structures:
        for worker in struct.workers:
            for vacation in worker.vacations:
                if vacation.isMorning and int(worker.work_id) in schedule[int(vacation.day) - 1][0]:
                    invalidTimeSlots += 1
                elif (not vacation.isMorning) and int(worker.work_id) in schedule[int(vacation.day) - 1][1]:
                    invalidTimeSlots += 1

    return (totalTimeSlots - invalidTimeSlots) / totalTimeSlots


def evaluateStructures(time_slots, structures):
    structTimes = []

    for struct in structures:
        workedSlots = 0
        totalSlots = 0
        for worker in struct.workers:
            workedSlots += worker.hoursWorked
            if worker.isFullTime:
                totalSlots += time_slots
            else:
                totalSlots += int(time_slots / 2)

        minStructSlots = math.ceil(totalSlots / 3)

        if workedSlots >= minStructSlots:
            # print(workedSlots, ">=", minStructSlots)
            structTimes.append(1)
        else:
            # print(workedSlots, "<", minStructSlots)
            structTimes.append(0)
    # print(structTimes)

    return statistics.mean(structTimes)


def evaluate(schedule, scheduleObj, structures):
    """
    Evaluate schedule based on three criterion.

    :param schedule: schedule to be evaluated
    :param scheduleObj: schedule data
    :param structures: workplace data
    :return: evaluation score
    """
    overtime = evaluateOvertime(scheduleObj, structures)
    vacation = evaluateVacations(schedule, scheduleObj.dayNum * scheduleObj.spaceNum, structures)
    structure = evaluateStructures(scheduleObj.dayNum * scheduleObj.spaceNum, structures)

    return 0.4 * overtime + 0.4 * vacation + 0.2 * structure


def generateNeighborList(schedule, employeeList):
    neighbors = []
    for i, day in enumerate(schedule):
        for j, shift in enumerate(day):
            for k, desk in enumerate(shift):
                neighbor = np.copy(schedule)
                neighbor[i][j][k] = 0
                neighbors.append(neighbor)
                for worker in employeeList:
                    if worker not in schedule[i][j]:
                        neighbor = np.copy(schedule)
                        neighbor[i][j][k] = worker
                        neighbors.append(neighbor)
    return neighbors


def solve(structureObj, scheduleObj):
    # start timer
    start_time = time.perf_counter()

    # create empty schedule
    current_schedule = np.zeros([scheduleObj.dayNum, 2, scheduleObj.spaceNum]).astype(
        int)  # T days, 2 shifts per day, K desks

    # fill schedule with values, initialize as current best and current generation root
    current_schedule = initializeSchedule(current_schedule, structureObj)
    current_eval = evaluate(current_schedule, scheduleObj, structureObj)

    scheduleObj.shiftSchedule = current_schedule  # best schedule kept in object
    scheduleObj.evaluation = current_eval

    generation_root = current_schedule  # schedule from which neighbors are generated
    root_eval = current_eval

    # check if initial solution is a perfect one
    if scheduleObj.evaluation == 1:  # found a perfect solution. Program can end early
        print("Schedule: ", scheduleObj.shiftSchedule.tolist(),
              f"\nSolution evaluation: {scheduleObj.evaluation * 100}%")
        # end timer
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print("Perfect solve found in", elapsed_time)
        return current_schedule

    # create and fill expense line (line will be 10 elements long)
    queueLen = 10
    expenses = Queue(maxsize=queueLen)
    for i in range(queueLen):
        expenses.put(1 - scheduleObj.evaluation)

    # create masterlist of worker IDs for use in neighbor generation
    employeeIDs = []
    for struct in structureObj:
        for worker in struct.workers:
            employeeIDs.append(worker.work_id)

    # # create masterlist of best solutions
    # prevBests = []
    # prevBests.append(scheduleObj.shiftSchedule)
    #
    # # create list to keep track of generation tree
    # prevRoots = []
    # prevRoots.append(generation_root)

    # -----------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------INITIALIZATION COMPLETE---------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------

    # neighbor list generation for current root
    neighborhood = generateNeighborList(generation_root, employeeIDs)

    iterationCounter = 0

    while True:  # infinite without interuption
        # Only works because business logic for the task dictates a perfect solution must exist
        iterationCounter += 1
        if iterationCounter > max(100, scheduleObj.dayNum * scheduleObj.spaceNum * (len(employeeIDs)+1)*2):
            # ārkārtas situācija, lai programma neciklētos bezgalīgi
            # problēmas avots: ieciklējas ar vienu generation_root, jo netiek klāt pie jauna
            # Godīgi? ieciklējas lokālajos optimumos un nespēju izkulties pat ar visu izmaksu rindu
            break
        # Testa dati, lai pārbaudītu ciklēšanos
        # print("--")
        # print("Iteration", iterationCounter, "Neighborhood:", len(neighborhood))
        # print("Best:", scheduleObj.shiftSchedule.tolist(), "eval:", scheduleObj.evaluation)
        # print("Root:", generation_root.tolist())
        # print("--")

        current_eval = 0
        current_schedule = []
        # choose best in neighborhood
        for neighbor in neighborhood:
            newEval = evaluate(neighbor, scheduleObj, structureObj)
            if newEval == 1:  # found a perfect solution in neighborhood
                print("Schedule: ", neighbor.tolist(),
                      f"\nSolution evaluation: {newEval * 100}%")
                # end timer
                end_time = time.perf_counter()
                elapsed_time = end_time - start_time
                print("Perfect solve found in", iterationCounter, "iterations and time", elapsed_time)
                return current_schedule
            if newEval > current_eval:  # find best in neighborhood
                current_schedule = np.copy(neighbor)
                current_eval = newEval

        # evaluate solution, if better than best -> replace as best solution
        if scheduleObj.evaluation < current_eval:
            scheduleObj.shiftSchedule = np.copy(current_schedule)
            scheduleObj.evaluation = current_eval
            # print("new best", current_schedule.tolist())

        # if less expensive than root or first-in-line, replace as new generation root
        # print(current_eval, root_eval)
        if current_eval > root_eval or current_eval > expenses.get():
            generation_root = np.copy(current_schedule)
            root_eval = current_eval
            # prevRoots.append(np.copy(generation_root))
            # print("new root", generation_root.tolist())
            # print("rootLen:", len(prevRoots))

        # put evaluation in expense line
        if expenses.qsize() == queueLen:
            expenses.get()
        expenses.put(current_eval)

        if current_eval == 1:  # found a perfect solution. Program can end early
            print("Schedule: ", scheduleObj.shiftSchedule.tolist(),
                  f"\nSolution evaluation: {current_eval * 100}%")
            # end timer
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            print("Perfect solve found in", iterationCounter, "iterations and time", elapsed_time)
            return current_schedule

        neighborhood = generateNeighborList(generation_root, employeeIDs)
        # print("new neighborhood generated")

    # end timer
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print("Schedule: ", scheduleObj.shiftSchedule.tolist(),
          f"\nSolution evaluation: {evaluate(scheduleObj.shiftSchedule, scheduleObj, structureObj) * 100}%")
    print("Imperfect solve called after", iterationCounter, "iterations and time", elapsed_time)
    return scheduleObj.shiftSchedule
