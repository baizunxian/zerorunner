# sys
from autotest.views.system.user import bp as user
from autotest.views.system.menu import bp as menu
from autotest.views.system.roles import bp as roles
from autotest.views.system.file import bp as file
# api
from autotest.views.api.project import bp as project
from autotest.views.api.module import bp as module
from autotest.views.api.env import bp as env
from autotest.views.api.timed_tasks import bp as timed_tasks
from autotest.views.api.test_case import bp as test_case
from autotest.views.api.debug_talk import bp as debug_talk
from autotest.views.api.test_report import bp as test_report
from autotest.views.api.test_suites import bp as test_suites


def register_app(app):
    # sys
    app.register_blueprint(user)
    app.register_blueprint(menu)
    app.register_blueprint(roles)
    app.register_blueprint(file)
    # api
    app.register_blueprint(project)
    app.register_blueprint(module)
    app.register_blueprint(env)
    app.register_blueprint(timed_tasks)
    app.register_blueprint(test_case)
    app.register_blueprint(debug_talk)
    app.register_blueprint(test_report)
    app.register_blueprint(test_suites)
