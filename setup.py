# copyright 2022 Medicines Discovery Catapult
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


def readme():
    with open("README.md") as f:
        return f.read()


__version__ = ""
exec(open("src/klein_config/version.py").read())
if __version__ == "":
    raise RuntimeError("unable to find application version")

setup(
    name="klein_config",
    version=__version__,
    description="Configuration detection from the command line",
    url="http://gitlab.mdcatapult.io/informatics/klein/klein-config",
    author="Matt Cockayne",
    author_email="matthew.cockayne@md.catapult.org.uk",
    license="MIT",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=["pyhocon", "pyyaml<6,>=5.1"],
    zip_safe=True,
)
