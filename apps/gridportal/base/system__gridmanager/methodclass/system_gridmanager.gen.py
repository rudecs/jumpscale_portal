from JumpScale import j

class system_gridmanager(j.code.classGetBase()):
    """
    gateway to grid
    """
    def __init__(self):
        pass
        
        self._te={}
        self.actorname="gridmanager"
        self.appname="system"
        #system_gridmanager_osis.__init__(self)


    def getDisks(self, id, guid, gid, nid, fs, sizeFrom, sizeTo, freeFrom, freeTo, mounted, ssd, path, model, description, mountpoint, type, active, lastcheckFrom, lastcheckTo, **kwargs):
        """
        list found disks (are really partitions) (comes from osis)
        param:id find based on id
        param:guid find based on guid
        param:gid find disks for specified grid
        param:nid find disks for specified node
        param:fs ext4;xfs;...
        param:sizeFrom in MB
        param:sizeTo in MB
        param:freeFrom in MB
        param:freeTo in MB
        param:mounted is disk mounted
        param:ssd is disk an ssd
        param:path match on part of path e.g. /dev/sda
        param:model match on part of model
        param:description match on part of description
        param:mountpoint match on part of mountpoint
        param:type type e.g. BOOT DATA CACHE
        param:active True,is the disk still active
        param:lastcheckFrom -4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find disks with lastcheckFrom  (-4d means 4 days ago)
        param:lastcheckTo -4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find disk with lastcheckTo  (-4d means 4 days ago)
        result list(list)
        """
        #put your code here to implement this method
        raise NotImplementedError ("not implemented method getDisks")

    def getGrids(self, **kwargs):
        """
        list grids
        result list(list)
        """
        #put your code here to implement this method
        raise NotImplementedError ("not implemented method getGrids")

    def getJob(self, id, guid, **kwargs):
        """
        gets relevant info of job (also logs)
        can be used toreal time return job info
        param:id obliged id of job
        param:guid find based on guid
        """
        #put your code here to implement this method
        raise NotImplementedError ("not implemented method getJob")

    def getJobs(self, id, guid, from_, to, nid, gid, parent, roles, state, organization, name, description, category, source, **kwargs):
        """
        interface to get job information
        param:id only find 1 job entry
        param:guid find based on guid
        param:from_ -4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find jobs from date specified  (-4d means 4 days ago)
        param:to -4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find jobs to date specified
        param:nid find jobs for specified node
        param:gid find jobs for specified grid
        param:parent find jobs which are children of specified parent
        param:roles match on comma separated list of roles (subsets also ok e.g. kvm.  would match all roles starting with kvm.)
        param:state OK;ERROR;...
        param:organization 
        param:name 
        param:description any description when asked for the job
        param:category category in dot notation
        param:source who asked for the job is free text
        """
        #put your code here to implement this method
        raise NotImplementedError ("not implemented method getJobs")

    def getLogs(self, id, level, category, text, to, jid, nid, gid, pid, tags, from_='-1h', **kwargs):
        """
        interface to get log information
        param:id only find 1 log entry
        param:level level between 1 & 9; all levels underneath are found e.g. level 9 means all levels
        param:category match on multiple categories; are comma separated
        param:text match on text in body
        param:from_ -4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find logs from date specified  (-4d means 4 days ago) default=-1h
        param:to -4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find logs to date specified
        param:jid find logs for specified jobid
        param:nid find logs for specified node
        param:gid find logs for specified grid
        param:pid find logs for specified process (on grid level)
        param:tags comma separted list of tags/labels
        """
        #put your code here to implement this method
        raise NotImplementedError ("not implemented method getLogs")

    def getNodes(self, id, guid, gid, name, roles, ipaddr, macaddr, active, peer_stats, peer_log, peer_backup, lastcheckFrom, lastcheckTo, **kwargs):
        """
        list found nodes (comes from osis)
        param:id find specific id
        param:guid find based on guid
        param:gid find nodes for specified grid
        param:name match on text in name
        param:roles match on comma separated list of roles (subsets also ok e.g. kvm.  would match all roles starting with kvm.)
        param:ipaddr comma separated list of ip addr to match against
        param:macaddr comma separated list of mac addr to match against
        param:active True,is the node still active
        param:peer_stats id of node which has stats for this node
        param:peer_log id of node which has logs (e.g. transactionlogs) for this node
        param:peer_backup id of node which has backups for this node
        param:lastcheckFrom -4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find nodes with lastcheckFrom  (-4d means 4 days ago)
        param:lastcheckTo -4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find nodes with lastcheckTo  (-4d means 4 days ago)
        result list(list)
        """
        #put your code here to implement this method
        raise NotImplementedError ("not implemented method getNodes")

    def getStatImage(self, statKey, width, height, **kwargs):
        """
        get png image as binary format
        comes from right processmanager
        param:statKey e.g. n1.disk.mbytes.read.sda1.last
        param:width 500,
        param:height 200,
        result binary
        """
        #put your code here to implement this method
        raise NotImplementedError ("not implemented method getStatImage")

    def getVDisks(self, id, machineid, guid, gid, nid, disk_id, fs, sizeFrom, sizeTo, freeFrom, freeTo, sizeondiskFrom, sizeondiskTo, mounted, path, description, mountpoint, role, type, order, devicename, backup, backuplocation, backuptime, backupexpiration, active, lastcheckFrom, lastcheckTo, **kwargs):
        """
        list found vdisks (virtual disks like qcow2 or sections on fs as used by a container or virtual machine) (comes from osis)
        param:id find based on id
        param:machineid to which machine is the vdisk attached
        param:guid find based on guid
        param:gid find vdisks for specified grid
        param:nid find vdisks for specified node
        param:disk_id find disk which hosts this disk
        param:fs ext4;xfs;...
        param:sizeFrom in MB
        param:sizeTo in MB
        param:freeFrom in MB
        param:freeTo in MB
        param:sizeondiskFrom in MB
        param:sizeondiskTo in MB
        param:mounted is disk mounted
        param:path match on part of path e.g. /dev/sda
        param:description match on part of description
        param:mountpoint match on part of mountpoint
        param:role type e.g. BOOT DATA CACHE
        param:type type e.g. QCOW2 FS
        param:order when more vdisks linked to a vmachine order of linkage
        param:devicename if known device name in vmachine
        param:backup is this a backup image
        param:backuplocation where is backup stored (tag based notation)
        param:backuptime epoch when was backup taken
        param:backupexpiration when does backup needs to expire
        param:active True,is the disk still active
        param:lastcheckFrom -4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find vdisks with lastcheckFrom  (-4d means 4 days ago)
        param:lastcheckTo -4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find vdisks with lastcheckTo  (-4d means 4 days ago)
        result list(list)
        """
        #put your code here to implement this method
        raise NotImplementedError ("not implemented method getVDisks")
