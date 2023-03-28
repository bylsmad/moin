# Copyright: 2012 MoinMoin:HughPerkins
# License: GNU GPL v3 (or any later version), see LICENSE.txt for details.

"""
Contains events called by pytest during the life-cycle of the test suite
This module is automatically loaded by pytest, which looks for a file
of this name
"""

import logging
import os
import pytest
from selenium import webdriver
import signal
import socket
import subprocess
import sys
from time import sleep

from . import config
from . import driver_register


def pytest_runtest_makereport(item, call):
    """
    Entry point for event which occurs after each test has run
    The parameters are:
    - item: the method called
    - call: an object of type CallInfo, which has two properties, of which
      excinfo contains info about any exception that got thrown by the method
    This method is called automatically by pytest.  The name of the method
    is used by pytest to locate it, and decide when to call it
    This specific method instance is used to take a screenshot whenever a test
    fails, ie whenever the method throws an exception
    """
    if call.excinfo is not None:
        if driver_register.get_driver() is not None and hasattr(item, 'obj'):
            outFile = os.path.join(os.path.dirname(__file__), str(item.obj).split(" ")[2] + '.html')
            with open(outFile, 'w') as f:
                f.write(driver_register.get_driver().page_source)


logger = logging.getLogger(__name__)


# copied from moin._tests
def check_connection(port, host='127.0.0.1'):
    """
    Check if we can make a connection to host:port.

    If not, raise Exception with a meaningful msg.
    """
    try:
        s = socket.create_connection((host, port))
        s.shutdown(socket.SHUT_RDWR)
        s.close()
    except socket.error as err:
        raise Exception("connecting to {0}:{1:d}, error: {2!s}".format(host, port, err))


# adapted from moin._tests.sitetesting.conftest
@pytest.fixture(scope="package")
def server():
    started = False
    try:
        check_connection(9080)
    except Exception:
        pass
    else:
        started = True
    if started:  # during development allow for running server manually started with run_moin.py
        yield started
    else:
        logger.info('starting server')
        server = None
        cwd = os.getcwd()
        my_dir = os.path.join(os.path.dirname(__file__), '..', 'src', 'moin', '_tests', 'sitetesting')
        os.chdir(my_dir)
        try:
            server_log = open('ui-server.log', 'wb')
            flags = 0
            if sys.platform == 'win32':
                flags = subprocess.CREATE_NEW_PROCESS_GROUP  # needed for use of os.kill
            com = ['python', './run_moin.py', '--no-load-help', '--backup-wiki']
            server = subprocess.Popen(com, stdout=server_log, stderr=subprocess.STDOUT,
                                      creationflags=flags)
            wait_count = 0
            while not started and wait_count < 12:
                wait_count += 1
                sleep(5)
                try:
                    check_connection(9080)
                except Exception as e:
                    logger.info(f'waiting for server startup {e}')
                else:
                    started = True
        finally:
            os.chdir(cwd)

        if started:  # if not started, clean up now
            yield started

        if not server:  # unexpected error
            logger.error(f'server is {server}')
            yield False
        else:
            if sys.platform == "win32":
                os.kill(server.pid, signal.CTRL_C_EVENT)
            else:
                server.send_signal(signal.SIGINT)
            try:
                server.communicate(timeout=10)
            except subprocess.TimeoutExpired:
                server.kill()
                server.communicate()
            server_log.close()
            if not started:
                logger.error('server not started. server.log:')
                os.chdir(my_dir)
                try:
                    with open(server_log.name) as f:
                        logger.error(f.read())
                finally:
                    os.chdir(cwd)
                yield started


@pytest.fixture(scope="package")
def driver(server):
    """
    Instantiates a chrome browser object, and configures it for English language
    and registers it for html capture, and sets the timeout
    """
    if not server:
        logger.error('server not started')
        yield None
    else:
        options = webdriver.ChromeOptions()
        options.add_argument("--lang=en")
        if 'GITHUB_RUN_NUMBER' in os.environ:
            # workaround for "DevToolsActivePort file doesn't exist" on github where tests run as root/Administrator
            options.add_argument("--no-sandbox")
            options.add_argument("--remote-allow-origins=*")
            options.add_argument("--disable-dev-shm-usage")
        if config.HEADLESS:
            options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        # prevent scrollable sidebar which interferes with ability to click OK button on Modify
        driver.set_window_size(500, 1080)
        driver_register.register_driver(driver)  # register with
        # driver_register, which is needed so that printscreen on test
        # failure works
        driver.implicitly_wait(20)
        yield driver
        driver.close()
