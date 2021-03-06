import multiprocessing
import time
import logging
from common_helper_process.fail_safe_subprocess import execute_shell_command_get_return_code

from helper import FIRMADYNE_PATH, ResultType


def start_emulation(result_dict, emulation_init_time):
    firmware_emulation = start_emulation_process_parallel(emulation_init_time)
    if not network_is_available(result_dict['ip']):
        result_dict.update({'emulation': ResultType.FAILURE, 'error_message': 'Firmadyne wasn\'t able to start the network while emulating'})
        return firmware_emulation
    result_dict.update({'emulation': ResultType.SUCCESS})
    return firmware_emulation


def start_emulation_process_parallel(emulation_init_time):
    emulation_process = multiprocessing.Process(name='firmware emulation', target=emulate_firmware)
    emulation_process.start()
    time.sleep(emulation_init_time)
    return emulation_process


def network_is_available(ip_address):
    output, rc = execute_shell_command_get_return_code('ping -c 1 {}'.format(ip_address), timeout=10)
    logging.debug('check_network:\/n{}'.format(output))
    if rc == 0 or '1 received' in output:
        return True
    else:
        return False


def emulate_firmware():
    logging.debug('start emulation')
    command = '{}/scratch/1/run.sh'.format(FIRMADYNE_PATH)
    output, _ = execute_shell_command_get_return_code(command)
    logging.debug('emulation output {}'.format(output))
