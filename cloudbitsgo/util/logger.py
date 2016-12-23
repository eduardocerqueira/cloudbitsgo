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

from logging import DEBUG, INFO, getLogger, Formatter, FileHandler


def get_logger(name, verbose=None):
    """Custom logging"""
    logger = getLogger(name)
    logger.propagate = False
    #handler = StreamHandler()
    handler = FileHandler('/tmp/cloudbitsgo.log')

    if verbose:
        console = ("%(asctime)s %(levelname)s "
                   "[%(name)s.%(funcName)s:%(lineno)d] %(message)s")
    else:
        console = ("%(asctime)s %(levelname)s %(message)s")

    # Set logging formatter
    formatter = Formatter(console, datefmt='%Y-%m-%d %H:%M:%S')

    handler.setFormatter(formatter)
    logger.handlers[:] = [handler]

    if verbose is True:
        logger.setLevel(DEBUG)
    else:
        logger.setLevel(INFO)
    return logger
