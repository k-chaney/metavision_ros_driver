# -----------------------------------------------------------------------------
# Copyright 2022 Bernd Pfrommer <bernd.pfrommer@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#

import launch
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration as LaunchConfig
from launch.actions import DeclareLaunchArgument as LaunchArg
from launch.actions import OpaqueFunction
from ament_index_python.packages import get_package_share_directory
import os


def launch_setup(context, *args, **kwargs):
    """Create simple node."""
    cam_name = LaunchConfig('camera_name')
    cam_str = cam_name.perform(context)
    pkg_name = 'metavision_ros_driver'
    share_dir = get_package_share_directory(pkg_name)
    trigger_config = os.path.join(share_dir, 'config', 'trigger_pins.yaml')
    bias_config = os.path.join(share_dir, 'config', 'silky_ev_cam.bias')
    node = Node(package='metavision_ros_driver',
                executable='driver_node',
                output='screen',
                # prefix=['xterm -e gdb -ex run --args'],
                name=cam_name,
                parameters=[
                    trigger_config,  # loads the whole file
                    {'use_multithreading': False,
                     'message_type': 'event_array',
                     'statistics_print_interval': 2.0,
                     'bias_file': bias_config,
                     'camerainfo_url': '',
                     'frame_id': '',
                     # 'roi': [315, 235, 20, 10],
                     # valid: 'enabled', 'loopback', 'disabled'
                     'trigger_in_mode': 'disabled',
                     # valid: 'enabled', 'disabled'
                     'trigger_out_mode': 'disabled',
                     'trigger_out_period': 100000,  # in usec
                     'trigger_duty_cycle': 0.5,     # fraction high/low
                     'trigger_message_time_threshold': 0.0,  # immediately
                     'event_message_time_threshold': 1.0e-3}],
                remappings=[
                    ('~/events', cam_str + '/events')])
    return [node]


def generate_launch_description():
    """Create simple node by calling opaque function."""
    return launch.LaunchDescription([
        LaunchArg('camera_name', default_value=['event_camera'],
                  description='camera name'),
        OpaqueFunction(function=launch_setup)
        ])
