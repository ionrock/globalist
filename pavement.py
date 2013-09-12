from paver.easy import *


options(
    venv=Bunch(dir='.'),
    test_reqs=[
        'pytest',
        'mock',
    ]
)

# local_options.py support
if path('local_options.py').exists():
    sys.path.append('.')
    import local_options
    options.update(local_options.options)


def env_do(tail, **kw):
    """Run a command from the virtualenv"""
    return sh('%s/bin/%s' % (options.venv.dir, tail), **kw)


@task
def virtualenv():
    sh('virtualenv %s' % options.venv.dir)


@task
@needs(['virtualenv'])
def bootstrap():
    env_do('python setup.py develop')
    for req in options.test_reqs:
        env_do('pip install %s' % req)


@task
def start():
    try:
        env_do('python globalist/server.py')
    except KeyboardInterrupt:
        pass
