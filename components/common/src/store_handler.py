import cassandra
import os
import time
from cassandra.cluster import Cluster


class StoreHandler:
    def __init__(self, should_create_schema=True):
        self.key_space = "my_key_space"
        self.session = self._create_session()
        if should_create_schema:
            self._ensure_key_space_exists()
            self._ensure_tables_exist()
        return

    def execute_query(self, query, params=()):
        return self.session.execute(query, params)

    def sentences_table_name(self):
        return self.key_space + ".sentences"

    def _create_session(self):
        cassandra_ip = os.environ['CASSANDRA_PORT_9042_TCP_ADDR']
        cassandra_port = os.environ['CASSANDRA_PORT_9042_TCP_PORT']
        # Sometimes Cassandra is still starting, so we might need to wait
        for _ in range(10):
            try:
                cluster = Cluster([cassandra_ip], port=cassandra_port)
                return cluster.connect()
            except cassandra.cluster.NoHostAvailable:
                time.sleep(20)
        cluster = Cluster([cassandra_ip], port=cassandra_port)
        return cluster.connect()

    def _ensure_key_space_exists(self):
        query = "CREATE KEYSPACE IF NOT EXISTS " + self.key_space + """ WITH
        REPLICATION = { 'class' : 'SimpleStrategy',
        'replication_factor' : 1 };"""
        self.execute_query(query)

    def _use_key_space(self):
        query = "USE " + self.key_space
        self.execute_query(query)

    def _ensure_tables_exist(self):
        self._ensure_sentences_tables_exist()

    def _ensure_sentences_tables_exist(self):
        languages = self._get_languages()
        for language in languages:
            query = self._language_table_specs(language)
            self.execute_query(query)

    def _get_languages(self):
        return os.environ['LANGUAGES'].split(":")

    def _language_table_specs(self, language):
        table_name = self.sentences_table_name()
        return "CREATE TABLE IF NOT EXISTS " + table_name + """ (
        language text,
        time timestamp,
        id uuid,
        author text,
        text text,
        primary key (language, time, id));"""
