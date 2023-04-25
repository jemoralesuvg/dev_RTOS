"""
Partitionned EDF using PartitionedScheduler.
"""
from simso.core.Scheduler import SchedulerInfo
from simso.utils import PartitionedScheduler
from simso.schedulers import scheduler

@scheduler("simso.schedulers.P_RM_FF")
class P_RM_FF(PartitionedScheduler):
    def init(self):
        PartitionedScheduler.init(
            self, SchedulerInfo("simso.schedulers.RM_mono"))

    def packer(self):
        # First Fit
        cpus = [[cpu, 0] for cpu in self.processors]
        numCPUs = len(cpus)
        assigned_tasks = [0] * numCPUs
        Urm = 0.0
        U = 0.0
        for task in self.task_list:
            #m = cpus[0][1]
            cpu_id = 0
            # Find if the new task will max the Urm and search cpu with space
            for i, c in enumerate(cpus):
                Urm = (assigned_tasks[i]+1.0) * ((pow(2.0, 1/(assigned_tasks[i]+1.0))) - 1.0)
                U = (c[1] + (task.wcet / task.period))
                if U < Urm:
                    cpu_id = i # available cpu
                    break

            assigned_tasks[cpu_id] = assigned_tasks[cpu_id] + 1
            # CPU scheduled = cpu_id

            # Affect it to the task.
            self.affect_task_to_processor(task, cpus[cpu_id][0])

            # Update utilization.
            cpus[cpu_id][1] += float(task.wcet) / task.period
        return True