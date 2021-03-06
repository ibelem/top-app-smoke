# -*- coding: utf-8 -*-

import os, sys
from datetime import *
from time import sleep
import time
from optparse import OptionParser
from script import common, adb, runtimelib, rundavinci, csvtoxml, gl
import threading

SUITEPATH = os.path.dirname(os.path.abspath(__file__))
TESTPATH = os.path.join(SUITEPATH,'tests')
SCRIPTPATH = os.path.join(SUITEPATH,'script')
JSONPATH = os.path.join(SCRIPTPATH, 'config.json')

rtlibapk = common.parse_c_json(JSONPATH, 'runtimelib_apk')
rtlibbuild = common.parse_c_json(JSONPATH, 'rtlib_test_build')
testresultdir = common.parse_c_json(JSONPATH, 'test_result_dir')

def l(str):
    common.log_info(str, gl.__logfile__)

def lr(str):
    common.log_err(str, gl.__logfile__)

def run(version, deviceid, arch):
    rundavinci.clear_davinci_test(deviceid)
    runtimelib.install_runtimelib(version, deviceid, arch)
    #time.sleep(5)
    rundavinci.run_davinci(version, deviceid, arch)
    csvtoxml.csv_xml(version, deviceid, arch)

def option_check(version, deviceid, arch):
    if arch and deviceid:
        arch = arch.lower()
        l('Device: ' + deviceid)
        l('Architecture: ' +  arch)
        run(version, deviceid, arch)
    elif arch and not deviceid:
        lr('Device id option is not defined.')
        lr('Use \'python run.py -h\' get more information.')
    elif deviceid and not arch:
        lr('Architecture option is not defined.')
        lr('Use \'python run.py -h\' get more information.')
    else:
        for i in common.parse_c_json(JSONPATH, 'device'):
            l('Device: ' + i['device_id'])
            l('Architecture: ' + i['device_arch'])
            l('Name: ' + i['device_name'])
            if not rtlibbuild:
                if version:
                    l('Version: ' + version)
                    run(version, i['device_id'], i['device_arch'])
                else:
                    lr('Version option is not defined.')
                    lr('Use -v or --version with the build number of '+ rtlibapk +'.')
                    sys.exit(0)
            else:
                for j in rtlibbuild:
                    run(j, i['device_id'], i['device_arch'])

def main():
    parser = OptionParser()
    parser.add_option('-v', '--version', dest='version',
                  help = '(optional) build number of ' + rtlibapk + '. if you don\'t specify it here, please make sure to add it in config.json.')
    #parser.add_option('-c', '--clear', dest='clear',
    #            help = '(optional) clear the test suite environment from the beginning.')
    parser.add_option('-a', '--arch', dest='arch',
                  help = '(optional) architecture (x86 or arm) of '+ rtlibapk +'. -d is required if you use it.')
    parser.add_option('-d', '--device', dest='device',
              help = '(optional) device ID of the test device. -a is required if you use it.')
    (options, args) = parser.parse_args()

    d = datetime.now()
    gl.__starttime__ = d.strftime('%Y-%m-%d %H:%M:%S')
    t = gl.__starttime__.replace(' ', '_').replace(':', '-')
    gl.__logfile__ = os.path.join(testresultdir, 'crosswalk_' + t + '.log')
    common.mk_dir(testresultdir)

    l('Device and test build information:')
    l('------------------------------------------------------------------------------------------------------------------------------------')

    option_check(options.version, options.device, options.arch)

if __name__ == '__main__':
    sys.exit(main())
    #python run.py -v 11.39.251.0 -a x86 -d MedfieldC3567E1E
