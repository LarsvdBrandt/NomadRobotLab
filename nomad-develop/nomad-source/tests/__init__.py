#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
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

"""
The nomad@FAIRDI tests are based on the pytest library. Pytest uses *fixtures* to
modularize setup and teardown of mocks, infrastructure, and other context objects.
The following depicts the used hierarchy of fixtures:

.. image:: /assets/test_fixtures.png

Otherwise the test submodules follow the names of the nomad code modules.
"""

from nomad.config import config


# This should be setup with fixtures with in conftest.py, but it will be too late.
# After importing the api/infrastructure module, the config values have already been used and
# changing them afterwards does not change anything anymore.

# For convinience we test the api without path prefix.
config.services.api_base_path = ''
