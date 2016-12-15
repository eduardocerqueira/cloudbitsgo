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

from action import Action, Report, CalcTime
from cloudbitsgo.util import get_args
from cloudbitsgo.util.logger import get_logger


def main():
    try:
        calctime = CalcTime()
        # Start execution
        start_time = calctime.start()
        mig_result = None
        args = get_args()
        log = get_logger(__name__, args.verbose)
        action = Action(args, start_time)

        if args.mig:
            mig_result = action.mig()

        # End execution
        calctime.end()
        hours, minutes, seconds = calctime.delta()
        log.info("End execution in %dh:%dm:%ds", hours, minutes, seconds)

    except Exception as ex:
        log.error(ex)

    finally:
        if mig_result:
            # Get summary report
            report = Report(calctime, mig_result, args)
            report.gen_summary()


if __name__ == '__main__':
    main()