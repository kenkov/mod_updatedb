#! /usr/bin/env python
# coding:utf-8


from mod import Mod
from logging import getLogger
from preprocessing import TwitterPreprocessing
from textfilter import JapaneseFilter
import pymongo as pm
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

        self.preprocess = TwitterPreprocessing()
        self.fltr = JapaneseFilter()
        client = pm.MongoClient(host, port)
        self.colld = client[db][coll]
        self.kov_colld = client["kovroid"]["tweet20150218"]

        self.dg = DepgenUpdateDB(
            host=host,
            port=port,
            db=db,
            coll=coll,
        )

    def is_utterance_needed(self, message, master):
        self.kov_colld.insert(message)

        text = message["text"]
        convtw = self.preprocess.convert(text)
        if self.fltr.is_passed(convtw):
            self.dg.update(convtw)

        return False

    def utter(self, message, master):
        return []
