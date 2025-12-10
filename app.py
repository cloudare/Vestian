from flask import Flask
import views.view as view
import time
from apscheduler.schedulers.background import BackgroundScheduler
import views.logWriter as lw

def schedule_run():
    lw.logBackUpRecord("Execution Started: "+str(time.strftime("%A, %d. %B %Y %I:%M:%S %p")))
    view.mainProcess() 
    lw.logBackUpRecord("Executed Successfully: "+str(time.strftime("%A, %d. %B %Y %I:%M:%S %p")))
    
#Scheduler    
sched = BackgroundScheduler(daemon=True)
# sched.add_job(schedule_run,'interval',seconds=10)
schedule_run()
sched.start()   
app = Flask(__name__)

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=8000)
    #app.run(debug=True,port=8000)