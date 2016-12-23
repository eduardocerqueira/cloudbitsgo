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

from os.path import exists
from cloudbitsgo.constant import SLINE, MLINE, RPTLINE
from cloudbitsgo.util.decorators import retry
from cloudbitsgo.util.logger import get_logger
from cloudbitsgo.util.dbreport import save_to_db
import sys
import subprocess
import os
import shutil
from time import time
from datetime import datetime, timedelta
import filecmp
import socket


class Action(object):
    """
    Hosting methods used by cloudbitsgo to perform action
    """

    def __init__(self, args, start_time):
        """Constructor"""
        self.args = args
        self.src = self.args.src
        self.dst = self.args.dst
        self.log = get_logger(__name__, args.verbose)
        self.start_time = datetime.fromtimestamp(start_time)
        # filter
        self.filter = None
        self.filter_pattern = None

        if self.args.filter and self.args.filter[0] \
            in ['ex', 'lst', 'sz', 'bw'] \
                and self.args.filter.__len__() >= 2:
                self.filter = self.args.filter[0]
                self.args.filter.remove(self.args.filter[0])
                self.filter_pattern = self.args.filter
        else:
            self.filter = None

        # verbose
        if self.args.verbose:
            self.verbose = self.args.verbose
            self.cp_verbose = '-v'
        else:
            self.verbose = None
            self.cp_verbose = ''

        self.print_cmd()

    def print_cmd(self):
        """Print the command line and all parameters being executed."""
        self.log.info(SLINE)
        self.log.info('args %s', self.args)
        self.log.info(SLINE)

    def is_src(self):
        """Check src is accessible."""
        # validate src
        if not exists(self.src):
            self.log.error("src %s doestn't exist", self.src)
            sys.exit(1)
        return True

    def get_dir_size(self):
        """Get size of src folder."""
        self.is_src()
        self.log.info('Calculating size of %s', self.src)
        cmd = ['du', '-s', self.src]
        dir_size = subprocess.check_output(cmd).replace(self.src, '')
        return dir_size

    def convert(self, dir_size):
        """Convert dir_size from KB to MB and GB"""
        _unit = 'MB'
        _raw_size = int(dir_size)

        # convert to GB
        if _raw_size > 1048576:
            _unit = 'GB'
            _size = _raw_size / 1048576

        # convert to MB
        if _raw_size < 1048576:
            _unit = 'MB'
            _size = _raw_size / 1024

        self.log.info('TOTAL %s%s', _size, _unit)
        return {'size': _size, 'unit': _unit, 'raw': _raw_size}

    def read_src(self):
        """Read all data from src folder, it is needed to apply filters and
        for summarize the process at the end of execution."""
        self.is_src()
        dir_size = self.get_dir_size()
        dir_size_converted = self.convert(dir_size)
        self.log.info('Loading files from %s', self.src)

        # SMALL  < 500 MB or 500,000 KB
        # MEDIUM < 100 GB or 104,857,600 KB
        # LARGE  > 100 GB or 104,857,600 KB

        if dir_size_converted['raw'] > 500000:
            self.log.info(MLINE)
            self.log.info('This can take several minutes to complete')
            self.log.info(MLINE)

        file_mig = []
        # read every individual file from src path
        for root, dirs, files in os.walk(self.src):
            for file_name in files:
                src_full_path = os.path.join(root, file_name)
                if self.custom_filter(src_full_path):
                    src_dir = root
                    dst_dir = root.replace(self.src, self.dst)
                    dst_full_path = os.path.join(dst_dir, file_name)
                    file_mig.append({'src_dir': src_dir,
                                     'dst_dir': dst_dir,
                                     'src_full_path': src_full_path,
                                     'dst_full_path': dst_full_path
                                     })

        self.log.info('TOTAL of %s files', file_mig.__len__())
        dir_size_formatted = '%s%s' % (dir_size_converted['size'],
                                       dir_size_converted['unit'])
        return file_mig, dir_size_formatted

    @retry(Exception, tries=3, delay=10)
    def run(self, fmig):
        """Manage the individual file migration"""
        _fmig_complete = False
        _error = 0
        _fname = fmig['src_full_path']
        _success = 0
        _linked = False

        try:
            # don't do anything, src symbolic link already pointing to dst
            if os.path.islink(fmig['src_full_path']):
                if fmig['dst_full_path'] in os.readlink(fmig['src_full_path']):
                    _linked = True
                    _success = 1
                    return True

            while(_fmig_complete is False):
                # create folder/subfolder at destination
                if(os.path.exists(fmig['dst_dir']) is False):
                    os.makedirs(fmig['dst_dir'], 0755)
                    # fix permissions based on src
                    shutil.copystat(fmig['src_dir'], fmig['dst_dir'])

                # copy file from src to dst
                shutil.copy2(fmig['src_full_path'], fmig['dst_full_path'])
                # fix permissions based on src
                shutil.copystat(fmig['src_full_path'], fmig['dst_full_path'])

                # check file
                if filecmp.cmp(fmig['src_full_path'], fmig['dst_full_path']):
                    _fmig_complete = True
                else:
                    os.remove(fmig['dst_full_path'])
                    _fmig_complete = False

            # delete file on source
            os.remove(fmig['src_full_path'])

            # set symbolic link
            os.symlink(fmig['dst_full_path'], fmig['src_full_path'])

            _linked = True
            _success = 1

        except Exception as ex:
            self.log.error(ex)
            _error = 1
        finally:
            _result = {'success': _success,
                       'linked_src_dst': _linked,
                       'error': _error,
                       'file_name': _fname
                       }

            # save into database for monitoring migration
            save_to_db(_result['file_name'], _result['success'],
                       _result['error'], _result['linked_src_dst'],
                       fmig['dst_full_path'], fmig['src_full_path'])

            return _result

    def custom_filter(self, scr_file=None):
        """
        Custom filter

        * by extension
            --filter ex *.png *.jpg

        * by last X hour(s) ACU [ Accessed, Created, Updated ]
            files Created in last 1 hour
            --filter lst 1 C

        * by size <>= X MB
            files less than 1MB
            --filter sz < 1MB

            files greater than or equal 1MB
            --filter sz >= 1MB

        TODO: not implemented yet
        * between DATE and DATE ACU [ Accessed, Created, Updated ]
            files Created between 2016-12-01 and 2016-12-31
            --filter bw 20161201 20161231

        """
        if self.args.filter is None:
            return True

        # by extension
        if 'ex' in self.filter:
            if scr_file.lower().endswith(tuple(self.filter_pattern)):
                return True

        # by lst (changes)
        if 'lst' in self.filter:
            # Time of last access
            if 'a' in self.filter_pattern[1]:
                filetime = datetime.fromtimestamp(os.path.getatime(scr_file))

            # The ctime as reported by the operating system. On some systems
            # (like Unix) is the time of the last metadata change, and, on
            # others (like Windows), is the creation time
            if 'c' in self.filter_pattern[1]:
                filetime = datetime.fromtimestamp(os.path.getctime(scr_file))

            # Time of last modification.
            if 'u' in self.filter_pattern[1]:
                filetime = datetime.fromtimestamp(os.path.getmtime(scr_file))

            _delta = self.start_time - \
                timedelta(days=int(self.filter_pattern[0]))

            if filetime > _delta:
                return True

        # by sz (size)
        if 'sz' in self.filter:
            # get the size, in bytes
            file_size = os.path.getsize(scr_file)

            if 'mb' in self.filter_pattern[2] or \
                    'MB' in self.filter_pattern[2]:
                    file_size = file_size / 1048576

            if 'gb' in self.filter_pattern[2] or \
                    'GB' in self.filter_pattern[2]:
                    file_size = file_size / 1073741824

            if '>' in self.filter_pattern[0]:
                if file_size > float(self.filter_pattern[1]):
                    return True

            if '<' in self.filter_pattern[0]:
                if file_size < float(self.filter_pattern[1]):
                    return True

            if '>=' in self.filter_pattern[0]:
                if file_size >= float(self.filter_pattern[1]):
                    return True

            if '<=' in self.filter_pattern[0]:
                if file_size <= float(self.filter_pattern[1]):
                    return True

        return False

    def mig(self):
        """data migration, basically:
            - Copy file from src to dst preserving ownership, permissions and
            timestamp for each individual file. For more details see: man cp
            - Check file at dst and compare size from src
            - Delete file from src
            - Create symbolic link from src to dst
        """
        _files, dir_size = self.read_src()
        _total_files = _files.__len__()
        _each_rs = []

        for fmig in _files:
            _each_rs.append(self.run(fmig))

        _result = {'total_files': _total_files,
                   'dir_size': dir_size,
                   'each_fmig': _each_rs
                   }

        return _result


class CalcTime(object):
    """Calculate elapsed time."""

    def __init__(self):
        """Constructor """
        # time
        self.start_time = None
        self.end_time = None
        self.duration = None

    def start(self):
        """Set start time."""
        self.start_time = time()
        return self.start_time

    def end(self):
        """Set end time."""
        self.end_time = time()

    def delta(self):
        """Calculate time delta between start and end times.

        :return: Hours, minutes, seconds
        """
        elapsed = self.end_time - self.start_time
        hours = elapsed // 3600
        elapsed = elapsed - 3600 * hours
        minutes = elapsed // 60
        seconds = elapsed - 60 * minutes

        return hours, minutes, seconds


class Report(object):
    """Summary report."""

    def __init__(self, calctime, mig_result, args):
        """Constructor """
        self.calc_time = calctime
        self.total_files = mig_result['total_files']
        self.dir_size = mig_result['dir_size']
        # each_rs has file_name, success, error, linked_src_dst
        # for each individual file migrated
        self.each_fmig = mig_result['each_fmig']
        self.hostname = socket.gethostname()
        self.args = args

    def gen_summary(self):
        """Generate summary for execution."""

        # get total of success and error
        total_success = 0
        total_error = 0
        total_linked = 0
        for fmig in self.each_fmig:
            total_success += int(fmig['success'])
            total_error += int(fmig['error'])
            if fmig['linked_src_dst'] is True:
                total_linked += 1

        hours, minutes, seconds = self.calc_time.delta()

        with open('report.txt', 'a') as report:
            report.write(MLINE + '\n')
            report.write('HOSTNAME: %s\n' % self.hostname)
            report.write(MLINE + '\n')
            report.write('START TIME: %s\n' %
                         datetime.fromtimestamp(self.calc_time.start_time))
            report.write('END TIME:   %s\n' %
                         datetime.fromtimestamp(self.calc_time.end_time))
            report.write('DURATION:   %dh:%dm:%ds\n' %
                         (hours, minutes, seconds))
            report.write(MLINE + '\n')
            report.write('SRC: %s\n' % self.args.src)
            report.write('DST: %s\n' % self.args.dst)
            report.write('SRC DIR SIZE:   %s\n' % self.dir_size)
            report.write('TOTAL OF FILES: %s\n' % self.total_files)
            report.write(MLINE + '\n')
            report.write('SUCCESS: %s\n' % total_success)
            report.write('LINKED:  %s (nothing to do)\n' % total_linked)
            report.write('ERROR:   %s\n' % total_error)
            # add list of all successfully files migrated to dst
            self.add_to_report('success', report)
            # add list of not migrated files to dst
            if(total_error > 0):
                self.add_to_report('error', report)
            # end of report
            report.write(RPTLINE + '\n')

    def add_to_report(self, fstatus, freport):
        freport.write(MLINE + '\n')
        freport.write('LIST ' + fstatus.upper() + ' FILES ' + '\n')
        freport.write(MLINE + '\n')
        line_number = 1
        for fmig in self.each_fmig:
            if fmig[fstatus] == 1:
                freport.write(str(line_number) + ' ' +
                             fmig['file_name'] + '\n')
                line_number += 1
        freport.write(MLINE + '\n')
