######################################################################
# Copyright 2016, 2017 John Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################
"""
Pet Model that uses Redis

You must initlaize this class before use by calling inititlize().
This class looks for an environment variable called VCAP_SERVICES
to get it's database credentials from. If it cannot find one, it
tries to connect to Redis on the localhost. If that fails it looks
for a server name 'redis' to connect to.
"""

import os
import json
import logging
from redis import StrictRedis
from redis.exceptions import ConnectionError


class DataValidationError(Exception):
    """Custom Exception with data validation fails"""

    pass


class Pet(object):
    """Pet interface to database"""

    logger = logging.getLogger(__name__)
    redis = None

    def __init__(self, id=0, name=None, category=None, available=True):
        """Constructor"""
        self.id = int(id)
        self.name = name
        self.category = category
        self.available = available

    def save(self):
        """Saves a Pet in the database"""
        if self.name is None:  # name is the only required field
            raise DataValidationError("name attribute is not set")
        if self.id == 0:
            self.id = Pet.__next_index()
        Pet.redis.set(self.id, json.dumps(self.serialize()))

    def delete(self):
        """Deletes a Pet from the database"""
        Pet.redis.delete(self.id)

    def serialize(self):
        """serializes a Pet into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "available": self.available,
        }

    def deserialize(self, data):
        """deserializes a Pet my marshalling the data"""
        try:
            self.name = data["name"]
            self.category = data["category"]
            self.available = data["available"]
        except KeyError as error:
            raise DataValidationError("Invalid pet: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid pet: body of request contained bad or no data"
            )
        return self

    ######################################################################
    #  S T A T I C   D A T A B S E   M E T H O D S
    ######################################################################

    @classmethod
    def __next_index(cls):
        """Increments the index and returns it"""
        return cls.redis.incr("index")

    @classmethod
    def remove_all(cls):
        """Removes all Pets from the database"""
        cls.redis.flushall()

    @classmethod
    def all(cls):
        """Query that returns all Pets"""
        # results = [cls.from_dict(redis.hgetall(key)) for key in redis.keys() if key != 'index']
        results = []
        for key in cls.redis.keys():
            if key != "index":  # filer out our id index
                data = json.loads(cls.redis.get(key))
                pet = Pet(data["id"]).deserialize(data)
                results.append(pet)
        return results

    ######################################################################
    #  F I N D E R   M E T H O D S
    ######################################################################

    @classmethod
    def find(cls, pet_id):
        """Query that finds Pets by their id"""
        if cls.redis.exists(pet_id):
            data = json.loads(cls.redis.get(pet_id))
            pet = Pet(data["id"]).deserialize(data)
            return pet
        return None

    @classmethod
    def __find_by(cls, attribute, value):
        """Generic Query that finds a key with a specific value"""
        # return [pet for pet in Pet.__data if pet.category == category]
        cls.logger.info("Processing %s query for %s", attribute, value)
        if isinstance(value, str):
            search_criteria = value.lower()  # make case insensitive
        else:
            search_criteria = value
        results = []
        for key in Pet.redis.keys():
            if key != "index":  # filer out our id index
                data = json.loads(Pet.redis.get(key))
                # perform case insensitive search on strings
                if isinstance(data[attribute], str):
                    test_value = data[attribute].lower()
                else:
                    test_value = data[attribute]
                if test_value == search_criteria:
                    results.append(Pet(data["id"]).deserialize(data))
        return results

    @classmethod
    def find_by_name(cls, name):
        """Query that finds Pets by their name"""
        return cls.__find_by("name", name)

    @classmethod
    def find_by_category(cls, category):
        """Query that finds Pets by their category"""
        return cls.__find_by("category", category)

    @classmethod
    def find_by_availability(cls, available=True):
        """Query that finds Pets by their availability"""
        return cls.__find_by("available", available)

    ######################################################################
    #  R E D I S   D A T A B A S E   C O N N E C T I O N   M E T H O D S
    ######################################################################

    @classmethod
    def connect_to_redis(cls, hostname, port, password):
        """Connects to Redis and tests the connection"""
        cls.logger.info("Testing Connection to: %s:%s", hostname, port)
        cls.redis = StrictRedis(
            host=hostname,
            port=port,
            password=password,
            charset="utf-8",
            decode_responses=True,
        )

        try:
            cls.redis.ping()
            cls.logger.info("Connection established")
        except ConnectionError:
            cls.logger.warning("Connection Error from: %s:%s", hostname, port)
            cls.redis = None
        return cls.redis

    @classmethod
    def init_db(cls, redis=None):
        """
        Initialized Redis database connection

        This method will work in the following conditions:
          1) In IBM Cloud with Redis bound through VCAP_SERVICES
          2) With Redis running on the local server as with Travis CI
          3) With Redis --link in a Docker container called 'redis'
          4) Passing in your own Redis connection object

        Exception:
        ----------
          redis.ConnectionError - if ping() test fails
        """
        if redis:
            cls.logger.info("Using client connection...")
            cls.redis = redis
            try:
                cls.redis.ping()
                cls.logger.info("Connection established")
            except ConnectionError:
                cls.logger.error("Client Connection Error!")
                cls.redis = None
                raise ConnectionError("Could not connect to the Redis Service")
            return

        # Get the credentials from the IBM Cloud environment
        if "VCAP_SERVICES" in os.environ:
            cls.logger.info("Using VCAP_SERVICES...")
            vcap_services = os.environ["VCAP_SERVICES"]
            services = json.loads(vcap_services)
            creds = services["rediscloud"][0]["credentials"]
            cls.logger.info(
                "Conecting to Redis on host %s port %s",
                creds["hostname"],
                creds["port"],
            )
            cls.connect_to_redis(creds["hostname"], creds["port"], creds["password"])
        else:
            cls.logger.info("VCAP_SERVICES not found, checking REDIS_HOST for Redis")
            REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
            REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
            cls.connect_to_redis(REDIS_HOST, REDIS_PORT, None)
        if not Pet.redis:
            # if you end up here, redis instance is down.
            cls.logger.fatal("*** FATAL ERROR: Could not connect to the Redis Service")
            raise ConnectionError("Could not connect to the Redis Service")
