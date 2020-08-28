import pymongo

from bson.objectid import ObjectId


class IODatabase:
    def __init__(self, mongo_uri):
        self._client = pymongo.MongoClient(mongo_uri)
        self._db = self._client["io"]

        # Collections
        self.vms = self._db["vms"]
        self.users = self._db["users"]

    def create_vm(self, hostname, cores, ram, disk, user):
        """Create a new VM

        :param hostname: hostname of the VM
        :param cores: number of cores
        :param ram: amount of memory in gigabytes
        :param disk: amount of storage space in gigabytes
        :param user: user that owns the VM (Document ID)
        :return:
        """

        self.vms.insert_one({
            "hostname": hostname,
            "cores": cores,
            "ram": ram,
            "disk": disk,
            "users": []
        })

    def add_vm_user(self, vm, user):
        """Allow a user to control a VM

        :param vm: VM to add user to (Document ID)
        :param user: User to add to VM (Document ID)
        :return:
        """
        if not self.users.find_one({"_id": ObjectId(user)}):
            print("ERROR: User not found.")
            return

        self.vms.update_one({"_id": ObjectId(vm)}, {"$push": {"users": ObjectId(user)}})
