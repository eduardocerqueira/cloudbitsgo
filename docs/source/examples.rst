.. _examples:


Examples
========

1. migrating all files from /home/eduardo/tmp to /home/eduardo/tmp1 with no filter::

	cloudbitsgo --mig --src /home/eduardo/tmp --dst /home/eduardo/tmp1

2. migrating omly .png files from /home/eduardo/tmp to /home/eduardo/tmp1::

	cloudbitsgo --mig --src /home/eduardo/tmp --dst /home/eduardo/tmp1 --filter ex .png

3. migrating only files created in last 3 hours from /home/eduardo/tmp to /home/eduardo/tmp1::

	cloudbitsgo --mig --src /home/eduardo/tmp --dst /home/eduardo/tmp1 --filter lst 3 c

4. migrating only files <= 10MB from /home/eduardo/tmp to /home/eduardo/tmp1::

	cloudbitsgo --mig --src /home/eduardo/tmp --dst /home/eduardo/tmp1 --filter sz <= 10 mb

5. migrating all files from src to dst and forcing user and group to 1000. note you get the uid and gid at /etc/group

	sudo cloudbitsgo --mig --src /tmp/origin/Desktop/ --dst /tmp/destination/Desktop/ --uidgid 1000:1000

for more links consult `filters <filter.html>`_
