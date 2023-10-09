# def checkForEmptyDesk(schedule):
#     """
#     Retrieve list of all empty desks in schedule
#
#     :param schedule: current schedule
#     :return: bool for empty desks and list of all empty desks
#     """
#     desks = []
#     hasEmpty = False
#     for i, day in enumerate(schedule):
#         for j, shift in enumerate(day):
#             if 0 in shift:
#                 for k, desk in enumerate(shift):
#                     hasEmpty = True
#                     desks.append([i, j, k])
#     return hasEmpty, desks
#
#
# def generateNeighbor(schedule, structures, timeSlots):
#     # 1. are any workers overworked?
#     workerFound = False
#     if evaluateOvertime(schedule, structures) < 1:
#         for struct in structures:
#             for worker in struct.workers:
#                 if worker.isFullTime and worker.hoursWorked > schedule.dayNum * 2:
#                     workerFound = True
#                 elif (not worker.isFullTime) and worker.hoursWorked > schedule.dayNum:
#                     workerFound = True
#                 if workerFound:
#                     # find first instance of work, empty the table
#                     for i, day in enumerate(schedule):
#                         for j, shift in enumerate(day):
#                             if int(worker.work_id) in int(shift):
#                                 for k, desk in enumerate(shift):
#                                     schedule[i][j][k] = 0
#                                     worker.hoursWorked -= 1
#                                     return schedule
#                                 print("ERROR IN OVERTIME CHANGE, FINDING DESK")
#         print("ERROR IN OVERTIME CHANGE, NO STRUCT WITH OVERWORKED")
#     # 2. are any structures working online too much?
#     if evaluateStructures(timeSlots, structures) < 1:
#         minStructSlots = math.ceil(timeSlots / 3)
#         for struct in structures:
#             totalSlots = 0
#             for worker in struct.workers:
#                 totalSlots += worker.hoursWorked
#
#             if totalSlots < minStructSlots:  # first structure that doesn't have enough in-person time
#                 emptyExists, desks = checkForEmptyDesk(schedule)
#                 if emptyExists:
#                     for desk in desks:  # try to fill desks one by one
#                         for worker in struct.workers:
#                             if int(worker.work_id) not in int(
#                                     schedule[desk[0]][desk[1]]):  # ensure physically possible solution
#                                 schedule[desk[0]][desk[1]][desk[2]] = worker
#                                 return schedule
#                     # program reaches here if no workers in struct 1 can be put in any desk
#         # program reaches here if no worker in any struct can be placed in any empty desk
#         # only possible if there are more desks than workers
#         # (impossible in any realistic schedule, based on business logic)
#     # 3. are any workers scheduled during vacation?
#     if evaluateVacations(schedule, timeSlots, structures) < 1:
#         for struct in structures:
#             for worker in struct.workers:
#                 for vacation in worker.vacations:
#                     if vacation.isMorning:
#                         if worker.work_id in schedule[vacation.day - 1][0]:  # find worker scheduled improperly
#                             worker.hoursWorked -= 1
#                             for k, desk in enumerate(schedule):
#                                 if int(schedule[vacation.day - 1][0][k]) == worker.work_id:
#                                     schedule[vacation.day - 1][0][k] = 0
#                                     return schedule
#                     else:
#                         if worker.work_id in schedule[vacation.day - 1][1]:  # find worker scheduled improperly
#                             worker.hoursWorked -= 1
#                             for k, desk in enumerate(schedule):
#                                 if int(schedule[vacation.day - 1][1][k]) == worker.work_id:
#                                     schedule[vacation.day - 1][1][k] = 0
#                                     return schedule
#                 # program reaches here if a worker is scheduled properly
#             # program reaches here if all workers in a structure are scheduled properly
#         print("ERROR ENCOUNTERED IN VACATION CHANGE-UP")
#
#     print("ERROR IN GENERATION, NO PROBLEM DETECTED ON IMPERFECT ROOT")
#     return