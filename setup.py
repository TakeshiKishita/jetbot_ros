from setuptools import setup

package_name = 'jetbot_ros2'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    author='Takeshi Kishita',
    maintainer='Dustin Franklin',
    maintainer_email='dustinf@nvidia.com',
    description='The jetbot_ros2 package',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'jetbot_motors = ' + package_name + '.jetbot_motors:main'
        ],
    },
)
