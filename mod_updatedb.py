#! /usr/bin/env python
# coding:utf-8


from mod import Mod
from logging import getLogger
from textfilter import TwitterPreprocess
import pymongo as pm
import traceback
from depgen_updatedb import DepgenUpdateDB


class ModUpdateDB(Mod):
    def __init__(
        self,
        logger=None,
        host="localhost",
        port: int=27017,
        db: str="depgen",
        coll: str="twitter",
    ):
        self.logger = logger if logger else getLogger(__file__)

        self.preprocess = TwitterPreprocess()
        client = pm.MongoClient(host, port)
        self.colld = client[db][coll]
        self.kov_colld = client["kovroid"]["tweet"]

        self.dg = DepgenUpdateDB(
            host=host,
            port=port,
            db=db,
            coll=coll,
        )

    def is_fire(self, message, master):
        self.kov_colld.insert(message)

        text = message["text"]
        convtw = self.preprocess.sub(text)
        try:
            if self.preprocess.filter(convtw):
                self.dg.update(text)
        except:
            traceback.print_exc()

        return False

    def reses(self, message, master):
        return []
