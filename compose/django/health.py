#!/usr/bin/env python3

import argparse
import logging
import os.path
import sys

import elasticsearch
import google
import psycopg2
from environ import Env
from google.cloud import storage


class HealthCheck:

    def __init__(self):
        self._setup_logger()
        self._setup_args()
        self._setup_envs()

    def _setup_logger(self):
        elasticsearch.logger.setLevel(elasticsearch.logging.ERROR)
        self._logger = logging.getLogger()

    def _setup_envs(self):
        self.env = Env()

        if self.args.env_file:
            self._logger.info("Loading vars from %s" % self.args.env_file)
            self.env.read_env(self.args.env_file)
        else:
            self._logger.info("Using vars from the current environment")

    def _setup_args(self):
        parser = argparse.ArgumentParser(description='Healthchecks for Django Applications')

        parser.add_argument("--env-file", help="Path to an env file", default=os.environ.get('ENV_FILE', None))
        parser.add_argument("--disable-postgres", action='store_true')
        parser.add_argument("--disable-gbucket", action='store_true')
        parser.add_argument("--disable-elasticsearch", action='store_true')

        self.args = parser.parse_args()

    def postgres(self):
        try:
            psycopg2.connect(
                dbname=self.env("POSTGRES_DB"),
                user=self.env("POSTGRES_USER"),
                password=self.env("POSTGRES_PASSWORD"),
                host=self.env("POSTGRES_HOST"),
                port=self.env("POSTGRES_PORT"),
                connect_timeout=3
            )
        except psycopg2.OperationalError:
            self._logger.error("Postgres not reachable!")
            return False
        return True

    def elasticsearch(self):
        return True
        try:
            elasticsearch.Elasticsearch(
                hosts=self.env('ELASTICSEARCH_URL', default='http://elasticsearch:9200'),
                verify_certs=True
            ).cluster.health(timeout='5s')

        except (elasticsearch.exceptions.ConnectionError):
            self._logger.error("Elasticsearch not reachable!")
            return False
        return True

    def gbucket(self):
        if not os.path.isfile(self.env("GOOGLE_APPLICATION_CREDENTIALS")):
            self._logger.error("Google Service Account file doesn't exists!")
            return False

        storage_client = storage.Client()

        try:
            storage_client.get_bucket(
                self.env("DJANGO_GCP_STORAGE_BUCKET_NAME")
            )
        except google.api_core.exceptions.NotFound:
            self._logger.error("Bucket %s does not exist!" % self.env("DJANGO_GCP_STORAGE_BUCKET_NAME"))
            return False
        return True

    def run(self):
        if not self.args.disable_postgres:
            if not self.postgres():
                sys.exit(-1)

        if not self.args.disable_gbucket:
            if not self.gbucket():
                sys.exit(-1)

        if not self.args.disable_elasticsearch:
            if not self.elasticsearch():
                sys.exit(-1)

        self._logger.info("Application is healthy!")
        sys.exit(0)


if __name__== "__main__":
    logging.basicConfig(level=logging.INFO)
    HealthCheck().run()
