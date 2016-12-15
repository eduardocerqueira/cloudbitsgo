![copr build](https://copr.fedorainfracloud.org/coprs/eduardocerqueira/cloudbitsgo/package/cloudbitsgo/status_image/last_build.png)

# cloudbitsgo

MOTIVATION:

I needed to migrate > 500GB critical data from PRODUCTION [1] AWS EBS (Elastic Block Storage) to [2] EFS (Elastic File System). It was a PRODUCTION server not
running on HA mode and with more than 150k page views per month.

for more info:

[1] https://aws.amazon.com/ebs/
[2] https://aws.amazon.com/efs/

WHAT IS THIS?

Linux tool to help on files migration from a source to a destination verifing the file was copied properly and then create a simbolic link from source to destination
not interrupting access to file.

USAGE:

all files from /home/eduardo/tmp to /home/eduardo/tmp1 with no filters::

	cloudbitsgo --mig --src /home/eduardo/tmp --dst /home/eduardo/tmp1

all files from /home/eduardo/tmp and extension is .txt or .json or .jpg::

	cloudbitsgo --mig --src /home/eduardo/tmp --dst /home/eduardo/tmp1 --filter ex .txt .json .jpg

all files from /home/eduardo/tmp and created in last 1 hour::

	cloudbitsgo --mig --src /home/eduardo/tmp --dst /home/eduardo/tmp1 --filter lst 1 c

all files from /home/eduardo/tmp and size less or equal 1MB::

	cloudbitsgo --mig --src /home/eduardo/tmp --dst /home/eduardo/tmp1 --filter sz <= 1 mb


# For developer and contributers

This section describes how to build a new RPM for cloudbitsgo;
I use make so it requires basic packages in your machine I recommend: python-setuptools, python-sphinx, python-devel and gcc

## RPM / Build

	$ make

	Usage: make <target> where <target> is one of

	clean     clean temp files from local workspace
	doc       generate sphinx documentation and man pages
	test      run unit tests locally
	tarball   generate tarball of project
	rpm       build source codes and generate rpm file
	srpm      generate SRPM file
	all       clean test doc rpm
	flake8    check Python style based on flake8

Running from your local machine, you can generate your own RPM running:

	$ make rpm

and if your environment is setup properly you should have your RPM at: /home/user/git/cloudbitsgo/rpmbuild/RPMS/x86_64/cloudbitsgo-0.0.1-1.x86_64.rpm

cloudbitsgo is being built on Fedora Copr: https://copr.fedorainfracloud.org/coprs/eduardocerqueira/cloudbitsgo/builds/

running a new build:

	$ copr-cli build cloudbitsgo https://github.com/eduardocerqueira/cloudbitsgo/raw/master/copr/cloudbitsgo-0.0.1-1.src.rpm


## install

Installing from your local machine, after you build your own RPM just run:

for Fedora:

	$ sudo dnf install /home/user/git/cloudbitsgo/rpmbuild/RPMS/x86_64/cloudbitsgo-0.0.1-1.x86_64.rpm

for RHEL and CentOS:

	$ sudo yum install /home/user/git/cloudbitsgo/rpmbuild/RPMS/x86_64/cloudbitsgo-0.0.1-1.x86_64.rpm

To install from latest RPM:

**repo:** https://copr-be.cloud.fedoraproject.org/results/eduardocerqueira/cloudbitsgo/fedora-24-x86_64/00474191-cloudbitsgo/

	$ sudo dnf install https://copr-be.cloud.fedoraproject.org/results/eduardocerqueira/cloudbitsgo/fedora-24-x86_64/00474191-cloudbitsgo/cloudbitsgo-0.0.1-1.x86_64.rpm


sample of report:

![Preview](https://github.com/eduardocerqueira/cloudbitsgo/raw/master/docs/source/_static/report.png)


## MORE INFO

For others topics listed below, please generate the sphinx doc in your local machine running the command:

	$ make doc

and from a browser access: file:///home/user/git/cloudbitsgo/docs/build/html/index.html

* Install:
* Guide:
* Build:
* Development:


 ## How to contribute

 Feel free to fork and send me pacthes or messages if you think this tool can be helpful for any other scenario.

