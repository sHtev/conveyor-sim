from setuptools import setup

setup(
   name='conveyor-sim',
   version='0.1',
   description='Simulate workers on an assembly line',
   author='Stephen Gilroy',
   author_email='code@shtev.dev',
   packages=['conveyor'],
   install_requires=['click'],
   entry_points='''
        [console_scripts]
        conveyor=conveyor.app:simulate
    '''
)