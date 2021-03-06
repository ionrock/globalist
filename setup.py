import setuptools


desc = open('README.rst').read()

setup_params = dict(
    name='Globalist',
    version='0.0.1',
    author='Eric Larson',
    author_email='eric@ionrock.org',
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'globalist = globalist.server:run',
        ]
    },
    install_requires=[
        'flask',
        'pyyaml',
        'requests',
        'cachecontrol',
        'pymongo>=2.6.2',
        'mgoquery>=0.5.4',
    ],
    description=desc,
)

if __name__ == '__main__':
    setuptools.setup(**setup_params)
