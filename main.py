import subprocess
import sys
import argparse

FETCH_LOGS_SCRIPT = "fetch_logs.sh"


def check_args(args=None):
    parser = argparse.ArgumentParser(description="Parsing the input arguments")
    parser.add_argument('-H', '--host', help='Server name', required=True)
    parser.add_argument('-u', '--username', help="Username to connect to the server", required=True)
    parser.add_argument('-f', '--filepath', help="complete file path", required=True)
    parser.add_argument('-p', '--pattern', help="search pattern", required=True)
    return parser.parse_args(args)


def fresh_run(arguments):
    print("Fresh Run")
    host = arguments.host
    user = arguments.username
    script_copy = ' '.join(['scp', "scripts/*", user + "@" + host + ":/home/" + user])
    print(f"Running Command = {script_copy}")
    session = subprocess.Popen(script_copy,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               universal_newlines=True,
                               bufsize=0, shell=True)
    (stdoutdata, stderrordata) = session.communicate()
    print(stdoutdata)
    print(stderrordata)
    print("Please confirm the script permission before proceeding")


def remote_run(arguments):
    host = arguments.host
    user = arguments.username
    filepath = arguments.filepath
    pattern = arguments.pattern
    fetch_logs_command = ' '.join(['sh', FETCH_LOGS_SCRIPT, pattern, filepath])
    out = []
    error = []
    ## if needed we can add multiple commands to the cmd_list and it will be executed sequentially
    cmd_list = [fetch_logs_command]
    ssh = ''.join([user, "@", host])
    print(f"ssh ={ssh}")
    for cmd in cmd_list:
        print(f"Running command = {cmd}")
        session = subprocess.Popen(["ssh "+ssh],
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   universal_newlines=True,
                                   bufsize=0,
                                   shell=True)
        (stdoutdata, stderrordata) = session.communicate(cmd)
        print(stdoutdata)
        print(stderrordata)
        out.append(stdoutdata)
        error.append(stderrordata)

        count = 0
        for result in out:
            with open(str(count) + ".txt", 'w') as filehandle:
                filehandle.writelines(result)
            count += 1


if __name__ == '__main__':
    args = check_args(sys.argv[1:])
    print('''   Enter 1 for Fresh run
    Fresh run will copy the required shell scrips to the remote server''')
    choice = input()
    if "1" == choice:
        fresh_run(args)
        print("Enter 2 to continue with file generation")
        choice_2 = input()
        if "2" == choice_2:
            remote_run(args)
    else:
        remote_run(args)
