from datetime import datetime, timedelta
import sublime
from sublime_plugin import ApplicationCommand, TextCommand
import time

class PomodoroStartCommand(TextCommand):

	"""todo: add support for user input if initiated using another shortcut"""
	# optionsForInterval = ["15 minutes", "20 minutes", "25 minutes", "30 minutes"]
	# optionsForBreak = ["5 minutes", "10 minutes"]
	# cycles = 4
	# optionsInSeconds = {
	# 	0: 15,
	# 	1: 1200,
	# 	2: 1500,
	# 	3: 1800,
	# }
	# breakTime = 15

	intervalTimeinSeconds = 0
	breakTimeinSeconds = 0
	cycles = 4

	def run(self, edit):
		#for testing purposes
		#sublime.pomodoro_clock = False	

		x = sublime.load_settings("pomodoro.sublime-settings")
		intervalTime = x.get("base_time",25)
		breakTime = x.get("breakTime",5)

		PomodoroStartCommand.cycles = x.get("cycles",4)
		PomodoroStartCommand.intervalTimeinSeconds = intervalTime*60
		PomodoroStartCommand.breakTimeinSeconds = breakTime*60

		if not hasattr(sublime, 'pomodoro_clock'):
			sublime.pomodoro_clock = True
		elif sublime.pomodoro_clock is True:
			sublime.error_message('Pomodoro Clock is already running, wait for the previous to stop first.')
			return
		else:
			sublime.pomodoro_clock = True

		if sublime.pomodoro_clock is True:
			PomodoroStartCommand.beginCycles(datetime.now(), timedelta(seconds = PomodoroStartCommand.intervalTimeinSeconds),PomodoroStartCommand.cycles)


	@staticmethod
	def beginCycles(startTime,countDownTime,cycles):
		if sublime.pomodoro_clock == True:
			PomodoroStartCommand.beginTimer(startTime,countDownTime)
			timeElapsed = PomodoroStartCommand.intervalTimeinSeconds*1000 #delay in milliseconds
			for c in range(1,cycles):
				sublime.set_timeout(lambda: PomodoroStartCommand.beginBreak(datetime.now(),timedelta(seconds=PomodoroStartCommand.breakTimeinSeconds)),timeElapsed)
				timeElapsed = timeElapsed + PomodoroStartCommand.breakTimeinSeconds*1000
				# print(timeElapsed/60)
				sublime.set_timeout(lambda: PomodoroStartCommand.beginTimer(datetime.now(),countDownTime),timeElapsed)
				timeElapsed = timeElapsed + PomodoroStartCommand.intervalTimeinSeconds*1000
				# print(timeElapsed/60)
			sublime.set_timeout(lambda: PomodoroStartCommand.reset(),timeElapsed)
		

	@staticmethod
	def reset():
		if (sublime.pomodoro_clock == False):
			sublime.status_message("Your pomodoro timer has been cancelled")
		else:
			sublime.pomodoro_clock = False
			sublime.status_message("Your pomodoro timer has ended.")
			sublime.message_dialog("Your pomodoro timer has ended. Take a well deserved break.")
		return
		# print("Everything ends")

					

	@staticmethod
	def beginTimer(startTime, countDownTime):
		if sublime.pomodoro_clock is True:
			timeLeft = (startTime - datetime.now()) + countDownTime
			sublime.status_message("time: {0}".format(timeLeft.total_seconds()))
			# breakTime = timedelta(seconds=20)
			flag = 0
			if timeLeft.total_seconds() > 0 and sublime.pomodoro_clock != False:
				PomodoroStartCommand.printStats(timeLeft,flag)
				sublime.set_timeout(lambda: PomodoroStartCommand.beginTimer(startTime, countDownTime),100)
			else:
				# print("Timer ends")
				return -1

	@staticmethod
	def beginBreak(startTime,countDownTime):
		if sublime.pomodoro_clock is True:
			timeLeft = (startTime - datetime.now()) + countDownTime
			sublime.status_message("time: {0}".format(timeLeft.total_seconds()))
			flag = 1
			if timeLeft.total_seconds() > 0 and sublime.pomodoro_clock != False:
				PomodoroStartCommand.printStats(timeLeft,flag)
				sublime.set_timeout(lambda: PomodoroStartCommand.beginBreak(startTime, countDownTime),100)
			else:
				# print("Break ends")
				return -1

	@staticmethod
	def printStats(timeElapsed,flag):
		seconds = timeElapsed.seconds
		minutes, seconds = divmod(seconds, 60)
		if flag==0:
			sublime.status_message("WORK: You have {0} minutes and {1} seconds before your break".format(minutes, seconds))
		else:
			sublime.status_message("BREAK : You have {0} minutes and {1} seconds before your start working again".format(minutes, seconds))

class PomodoroStopCommand(TextCommand):
	"""docstring for PomodoroStop"""
	def run(self, edit):
		sublime.pomodoro_clock=False
		sublime.status_message("Pomodoro clock has been stopped")
		return