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

import argparse
import sys


def get_args():
    """
    Get user args if exist;

    Arguments:

    --action: copy or move
    --src: source full path where files will be read
    --dst: destination full path where filles will be copyed or moved to
    --filter: string with multi-values args the filter rule accepts:
        ACU file is Accessed, Created, Updated
        AD  ascendant or descendant
        S <> X less than or greater than a value specified in MB
        between two dates
    """
    parser = argparse.ArgumentParser(prog='cloudbitsgo')
    required_named = parser.add_argument_group('required arguments')

    required_named.add_argument('--mig', default=True,
                                help="migrate data from src to dst",
                                required=True,
                                action='store_true')

    required_named.add_argument("--src",
                                help="source folder",
                                type=str,
                                required=True,
                                action='store')

    required_named.add_argument("--dst",
                                help="destination folder",
                                type=str,
                                required=True,
                                action='store')

    parser.add_argument("--uidgid",
                        help="set user id and group id to symbolic link, e.g:\
                        --uidgid 1000:1000",
                        type=str,
                        default=False,
                        action="store")

    parser.add_argument("--verbose",
                        help="run on verbose mode (DEBUG) level",
                        default=False,
                        action="store_true")

    # ex, lst, sz, bw
    parser.add_argument("--filter",
                        help="see find --help or check man page for examples",
                        nargs="*")

    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
        sys.exit(1)

    return args
