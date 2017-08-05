#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from logging import DEBUG, INFO, getLogger, Formatter, FileHandler, StreamHandler
import sys

def get_logger(name, verbose=None):
    """Custom logging"""
    logger = getLogger(name)
    logger.propagate = False
    file_handler = FileHandler('/tmp/cloudbitsgo.log')
    console_handler = StreamHandler(sys.stdout)

    if verbose:
        console = ("%(asctime)s %(levelname)s "
                   "[%(name)s.%(funcName)s:%(lineno)d] %(message)s")
    else:
        console = ("%(asctime)s %(levelname)s %(message)s")

    # Set logging formatter
    formatter = Formatter(console, datefmt='%Y-%m-%d %H:%M:%S')

    # Prepare multiple handlers (console and file)
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    if verbose is True:
        logger.setLevel(DEBUG)
    else:
        logger.setLevel(INFO)
    return logger
