.. _motivation:


Motivation
==========

I helped a buddy in a file migrate between two servers but it wasn't just a copy files from A to B! it was critical data from a PRODUCTION server running on [1] AWS so EC2 with a
large EBS (Elastic Block Storage) and the data needed to be migrated to [2] EFS (Elastic File System).

The PRODUCTION server wasn't running on HA (High-Availability) mode was reaching the disk space limit very quick, ah this server was serving a Webserver and hosting an web
application with more than 150k page views per month!

**Why not rsync?**

I am actually very familiar with rsync and use this in others scripts for backup my home-servers but the main reason was because rsync is slow and I wanted to move the file
at the end of process not just compare files and copy the content to destination.

so then I build this Linux tool to help on files migration from a source to a destination verifying the file was copied properly and then create a symbolic link from source
to destination not interrupting access to file.


for more info:

[1] https://aws.amazon.com/ebs/

[2] https://aws.amazon.com/efs/
