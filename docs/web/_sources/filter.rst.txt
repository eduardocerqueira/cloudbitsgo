.. _filter:


Filter
======

Types of filter:

* by extension

Accepts multiple formats separated by space.

usage:

all files from /home/eduardo/tmp and extension is .txt or .json or .jpg::

	cloudbitsgo --mig --src /home/eduardo/tmp --dst /home/eduardo/tmp1 --filter ex .txt .json .jpg

* by last X time ACU [ Accessed, Created, Updated ]

Filter files by Accessed, Created or Updated/Modified during a time. The time unit is HOUR

usage:

all files from /home/eduardo/tmp and created in last 1 hour::

	cloudbitsgo --mig --src /home/eduardo/tmp --dst /home/eduardo/tmp1 --filter lst 1 c

all files from /home/eduardo/tmp and modified in last 5 hours::

	cloudbitsgo --mig --src /home/eduardo/tmp --dst /home/eduardo/tmp1 --filter lst 5 u

all files from /home/eduardo/tmp and accessed in last 1 hour::

	cloudbitsgo --mig --src /home/eduardo/tmp --dst /home/eduardo/tmp1 --filter lst 1 a


* by size <>= X MB

Accepts arithmetic symbols to compare file size like: <,>,<=,>= and the unit can be MB or GB, lower case works too so mb, gb.

usage:

all files from /home/eduardo/tmp and size less or equal 1MB::

	cloudbitsgo --mig --src /home/eduardo/tmp --dst /home/eduardo/tmp1 --filter sz <= 1 mb

all files from /home/eduardo/tmp and size less or equal 1GB::

	cloudbitsgo --mig --src /home/eduardo/tmp --dst /home/eduardo/tmp1 --filter sz <= 1 gb
