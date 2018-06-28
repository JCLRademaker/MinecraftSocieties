from task import Task
from random import randint, choice


class ScoutTask(Task):
    def __init__(self, agent, infoGoal):
        Task.__init__(self, agent)
        self.goal = infoGoal
        self.counter = 0
        self.target = (0, 61, 0)
        self.target_reached = True
        
    def dist(self, coordinatesA, coordinatesB):
        # Manhattan distance, ignoring height.
        # Input: 2 (X,Y,Z) coordinate sets
        # Returns float distance.
        return abs(coordinatesA[0] - coordinatesB[0]) + abs(coordinatesA[2] - coordinatesB[2])
        
    def Execute(task, agent):
        if agent.InformationCount() >= task.goal:
            chests = agent.block_list["chest"]
            chestLocation = (chests[0][0] + 0.5, 60, chests[0][1] + 0.5)
            if agent.MoveToLocation(chestLocation, distance = 3):
                agent.SendCommand("move 0")
                return True
        else:
            if "worldGrid" in agent.data:
                blocks = agent.data.get(u'worldGrid', 0)
                agent.UpdateMapEfficient(blocks)
                task.counter+=1
                if task.counter == 1:
                    agent.UpdateMapFull(blocks)
                    task.target = (0, 61, 0)


            #Select a scouting destination, then move there:
            radius = 16
            min_score = 10**5
            while task.target_reached:
                old_target = task.target
                for i in range(int(radius/2)):
                    x = randint(-radius, radius)
                    z = choice([1,- 1])*(radius - abs(x))
                    check_coordinates = (old_target[0] + x, old_target[1], old_target[2] + z)
                    if not agent.CheckMap(check_coordinates):
                        score = task.dist(check_coordinates, agent.home)
                        if score < min_score:
                            task.target = check_coordinates
                            min_score = score
                            task.target_reached = False
                radius += 6
            agent.MoveToLocation(task.target)
            if task.dist(agent.Position, task.target) < 3:
                task.target_reached = True

    

