from setuptools import find_packages, setup

package_name = 'udp_joystick_bridge'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='edomo',
    maintainer_email='edomo@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
	    'udp_listener = udp_joystick_bridge.udp_listener:main',
	    'motor_driver = udp_joystick_bridge.motor_driver:main',
        ],
    },
)
