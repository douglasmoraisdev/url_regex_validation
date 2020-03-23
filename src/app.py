from concurrent.futures import ThreadPoolExecutor
from os import environ
from dotenv import load_dotenv
from utils.log_utils import log

load_dotenv()


class App:

    def __init__(self):
        self.max_workers = int(environ.get('MAX_WORKERS'))
        self.jobs = []
        self.log = log

    def run(self, *flows):

        self.log.info('Running App %s...' % environ.get('APP_NAME'))

        with ThreadPoolExecutor(self.max_workers) as executor:

            for flow in flows:
                self.jobs.append(executor.submit(flow.run))

        return self.jobs

    def close(self):

        self.log.info('Closing App %s' % environ.get('APP_NAME'))

        for job in self.jobs:
            job[1].__state = 'FINISH'
