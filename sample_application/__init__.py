import dateutil.parser

from flask import Flask, render_template, request
from flask_adminlte import AdminLTE
import data_process as dp
import os
import arcpy
import pandas as pd
from celery import Celery

class User(object):
    """
    Example User object.  Based loosely off of Flask-Login's User model.
    """
    full_name = "John Doe"
    avatar = "/static/img/user2-160x160.jpg"
    created_at = dateutil.parser.parse("November 12, 2012")


def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

def create_app(configfile=None):
    app = Flask(__name__)
    print str(app.import_name)
    app.config.update(
        CELERY_BROKER_URL='redis://localhost:6379',
        CELERY_RESULT_BACKEND='redis://localhost:6379'
    )
    celery = make_celery(app)
    AdminLTE(app)
    # This is a placeholder user object.  In the real-world, this would
    # probably get populated via ... something.
    current_user = User()

    @app.route('/')
    def index():
        return render_template('index.html', current_user=current_user)

    @app.route('/login')
    def login():
        return render_template('login.html', current_user=current_user)

    @app.route('/lockscreen')
    def lockscreen():
        return render_template('lockscreen.html', current_user=current_user)

    @app.route('/process_data')
    def process_data():
        return render_template('form_data.html', current_user=current_user)

    @app.route('/addRegion', methods=['POST'])
    def addRegion():
        #print(request.form['pre_flood'])
        #print(request.form['post_flood'])
        #print(request.form['out_directory'])
        #print(request.form['projected_shapefile'])
        print "eunha"

        # data_type = "Landsat8"

        # pre_flood = "C:/DATA_LAPAN/LC81190652016273LGN00"
        # post_flood = "C:/DATA_LAPAN/LC81190652017067RPI00"
        # out_process = "C:/DATA_LAPAN/LC81190652016273LGN00_OutputTools88"

        # #inFC = "C:/DATA_LAPAN/New_Shapefile.shp"

        # pre_flood = os.path.normpath(pre_flood)
        # post_flood = os.path.normpath(post_flood)
        # out_process = os.path.normpath(out_process)
        # # inFC = os.path.normpath(inFC)
        # #SR = arcpy.Describe(inFC).spatialReference
        # print(data_type)
        # print(pre_flood)
        # print(post_flood)
        # print(out_process)

        # masktype = "Cloud"
        # confidence = "High"
        # cummulative = 'false'

        # print(masktype)
        # print(confidence)

        # deltaNDWI = '0.11'
        # NDWIduring = '0.11'

        # os.mkdir(out_process)
        # some_list = [pre_flood, post_flood]
        # df = pd.DataFrame(some_list, columns=["colummn"])
        # df.to_csv(out_process+'/list.csv', index=False)
        # dp.mask_cloud(pre_flood, masktype, confidence, cummulative, out_process)
        # dp.mask_cloud(post_flood, masktype, confidence, cummulative, out_process)
        # #dp.process_landsat(pre_flood, SR, out_process, "_PreFlood", data_type, "")
        # #dp.process_landsat(post_flood, SR, out_process, "_PostFlood", data_type, "")
        result = add_together.delay(23, 42)
        result.wait()
        print result
        
        return "success"

    @celery.task()
    def add_together(a, b):
        return a + b
        data_type = "Landsat8"

        pre_flood = "C:/DATA_LAPAN/LC81190652016273LGN00"
        post_flood = "C:/DATA_LAPAN/LC81190652017067RPI00"
        out_process = "C:/DATA_LAPAN/LC81190652016273LGN00_OutputTools88"

        #inFC = "C:/DATA_LAPAN/New_Shapefile.shp"

        pre_flood = os.path.normpath(pre_flood)
        post_flood = os.path.normpath(post_flood)
        out_process = os.path.normpath(out_process)
        # inFC = os.path.normpath(inFC)
        #SR = arcpy.Describe(inFC).spatialReference
        print(data_type)
        print(pre_flood)
        print(post_flood)
        print(out_process)

        masktype = "Cloud"
        confidence = "High"
        cummulative = 'false'

        print(masktype)
        print(confidence)

        deltaNDWI = '0.11'
        NDWIduring = '0.11'

        os.mkdir(out_process)
        some_list = [pre_flood, post_flood]
        df = pd.DataFrame(some_list, columns=["colummn"])
        df.to_csv(out_process+'/list.csv', index=False)
        dp.mask_cloud(pre_flood, masktype, confidence, cummulative, out_process)
        dp.mask_cloud(post_flood, masktype, confidence, cummulative, out_process)
        #dp.process_landsat(pre_flood, SR, out_process, "_PreFlood", data_type, "")
        #dp.process_landsat(post_flood, SR, out_process, "_PostFlood", data_type, "")

    return app

if __name__ == '__main__':
    create_app().run(debug=True)
