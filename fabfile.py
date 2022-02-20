# coding: utf-8



from fabric import task


PROJECT_PATH = '/home/web/app'
PYTHON_PATH = '/home/web/app'
REQUIREMENTS = 'requirements.txt'


@task(default=True)
def full_deploy(c, branch=None):

    c.forward_agent = True
    with c.cd(PROJECT_PATH):
        checkout_to_branch(c, branch)
        get_latest_source(c)
        update_requirements(c, PYTHON_PATH)
        update_staticfiles(c, PYTHON_PATH)
        migrate(c, PYTHON_PATH)
        compile_messages(c, PYTHON_PATH)
    restart_supervisor_services(c)


@task
def checkout_to_branch(c, branch):
    current_branch = c.run('git rev-parse --abbrev-ref HEAD')
    if branch is None or branch == current_branch:
        return
    c.run('git fetch')
    c.run('git checkout {}'.format(branch))


@task
def get_latest_source(c):
    c.run('git log -n 1')  # print current commit
    c.run('git pull')


@task
def update_requirements(c, python_path):
    c.run('{} -m pip install -r {}'.format(python_path, REQUIREMENTS))


@task
def update_staticfiles(c, python_path):
    c.run('{} manage.py collectstatic --noinput'.format(python_path))


@task
def migrate(c, python_path):
    c.run('{} manage.py migrate'.format(python_path))


@task
def restart_supervisor_services(c):
    c.sudo('supervisorctl reload')


@task
def compile_messages(c, python_path):
    c.run("{} manage.py compilemessages".format(python_path))
