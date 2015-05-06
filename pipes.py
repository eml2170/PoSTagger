from subprocess import Popen, PIPE

class Procserver:
    '''
    Launch a python process that reads from stdin and writes to stdout as a
    service.
    '''
    def __init__(self, proc_args):
        '''
        Initializes the process using its arguments.
        '''
        self.proc = Popen(proc_args, stdout=PIPE, stdin=PIPE)

    def __del__(self):
        '''
        Terminates the process.
        '''
        self.proc.terminate()

    def communicate(self, string):
        '''
        Writes string to the process's stdin and blocks till the process writes
        to its stdout. Returns the contents from the process's stdout.
        '''
        self.proc.stdin.write(string.strip()+'\n\n')
        out = ''
        while True:
            line = self.proc.stdout.readline()
            if not line.strip(): break
            out += line
        return out.strip()
"""
if __name__ == '__main__':
    server = Procserver(['cat'])
    print server.communicate('test').strip()
    print server.communicate('test2').strip()
    """