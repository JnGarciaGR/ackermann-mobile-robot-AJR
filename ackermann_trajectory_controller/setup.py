from setuptools import find_packages, setup

package_name = 'ackermann_trajectory_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    package_data={'': ['py.typed']},
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ricardo-escudero',
    maintainer_email='ricardo-escudero@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': ['trajectory_publisher = ackermann_trajectory_controller.trajectory_publisher:main', 'odom_recorder = ackermann_trajectory_controller.odom_recorder:main',
        ],
    },
)
