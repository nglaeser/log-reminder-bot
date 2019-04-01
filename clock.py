from apscheduler.schedulers.blocking import BlockingScheduler
import app

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='sun', hour=22)
def scheduled_job():
  log_reminder()

def log_reminder():
  msg = 'Reminder to do your weekly logs!'
  app.send_message(msg)

sched.start()
