from setuptools import setup

setup(
    name='software_manager',
    version='0.1.0',
    packages=['software_manager', 'software_manager.libs',
              'software_manager.libs.dependencies',
              'software_manager.libs.dependencies.yaml'],
    url='',
    license='',
    author='hao.long',
    author_email='hoolongvfx@gmail.com',
    description='software manager',
    entry_points={
        # Using console script because the current use of print statements
        # leads to exceptions when no console is attached.
        'console_scripts': [
            'software_manager = software_manager.main',
        ]
    },

)
