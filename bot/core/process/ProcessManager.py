from .process import Process
import asyncio

class ProcessManager:
  def __init__(self):
      self.processes = {}
      self.next_id = 1

  def create_process(self, name):
      process_id = self.next_id
      self.next_id += 1
      process = Process(process_id, name)
      self.processes[process_id] = process
      return process

  def get_process(self, process_id):
      return self.processes.get(process_id)

  def stop_process(self, process_id):
      process = self.get_process(process_id)
      if process:
          asyncio.create_task(process.stop())
          del self.processes[process_id]

  def list_processes(self):
      return [process for process in self.processes.values() if process.is_running()]