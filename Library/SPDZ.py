'''
(C) 2017 Malte Kruse. See License.txt.
'''
import os, subprocess, multiprocessing, shutil
from . import communication as comm

class MPCProgram():
    
    lib_dir = os.path.dirname(os.path.realpath(__file__))
    main_dir = os.path.abspath(os.path.join(lib_dir, os.pardir))
    
    config = {}
    used = []
    
    outputs = {}
    counter = 0;
    
    ready = True;
    
    def __init__(self, program, player=0, max_player=2, port=5000, hostname='localhost', f2n=False):
        r""" Initialize a SPDZ-Computation and compile the specific \verb+program+ """
        self.program = program
        self.config['player'] = player
        self.config['max_player'] = max_player
        self.config['port'] = port
        self.config['hostname'] = hostname
        self.config['f2n'] = f2n
        
        self.output_queue = multiprocessing.Queue()
        self.input_queue = multiprocessing.Queue()

        os.chdir(self.main_dir)
        compilation = subprocess.Popen(["python2", "./compile.py", self.program])
        compilation.wait()

    def __internal_write_input_to_queue(self, obj):
        r'''Used by user process. The process can always write input to the queue.'''
        self.input_queue.put(obj)
    
    def __internal_get_output_from_queue(self):
        r'''Receive all Elements passed to the output queue. 
        
        If output queue is empty, wait until elements are passed to the queue.'''
        output = self.output_queue.get();
        self.outputs.update(output)
        
    def run(self):
        r""" Connect to server and run the program. Player \verb+0+ will always setup the Server."""
        
        if self.ready == False and self.mpc.is_alive():
            raise RuntimeError("The process is still running.")
        elif self.ready == False:
            raise RuntimeError("The Program is not ready. Please use clean() before new execution")
        
        os.chdir(self.main_dir)
        if self.config['player'] == 0:
           subprocess.Popen(["./Server.x", str(self.config['max_player']), str(self.config['port'])])

        self.mpc = multiprocessing.Process(target=comm.start_mpc, args=(self.main_dir, self.config, self.program, self.input_queue, self.output_queue))
        self.mpc.start() 
        self.ready = False;
    
    
    def clear(self):
        r'''Clears the Programs I/O and prepares the Program to rerun.

        If the previous MPC has not finished yet, the restart will wait until the current processed
        has finished.'''
        if self.mpc.is_alive():
            raise RuntimeError("The process is still running.")

        self.output_queue = multiprocessing.Queue()
        self.input_queue = multiprocessing.Queue()
        self.used = []
        self.outputs = {}
        self.counter = 0
        
        self.ready = True
        
    def configure(self, key, config):
        r'''Add or change a configuration.'''
        self.config[key] = config
    
    def get_private_output(self):
        r"""Get the content of the private output-file for the current player."""
        os.chdir(self.main_dir)
        
        file = open(self.main_dir + "/Player-Data/Private-Output-" + str(self.config['player']), "rb")
        result = file.read()
        file.close()
        
        os.chdir(self.lib_dir)
        return result;
    
    def get_public_output(self):
        r"""Get the content of the public output-file for the current player."""
        os.chdir(self.main_dir)
        
        file = open(self.main_dir + "/Player-Data/Public-Output-" + str(self.config['player']), "rb")
        result = file.read()
        file.close()
        
        os.chdir(self.lib_dir)
        return result;
    
    def get_output(self, token, line=0):
        r'''Returns the programs output related to the token. If the output isnt already passed to
        the user process, check the output queue.
        Use \verb+line+, if the token is connected to multiline output to specifiy which line is needed.'''
        while True:
            if token in self.outputs.keys():
                output = self.outputs[token]
                if isinstance(output, str):
                    return output
                else:
                    return output[line]
            else:
                self.__internal_get_output_from_queue()
    
    def pop_output(self, token, line=0):
        r'''Pops the programs output related to the token. If the output isnt already passed to
        the user process, check the output queue. The given token can be reused later on to generate new output.
        Use \verb+line+, if the token is connected to multiline output to specifiy which line is needed.'''
        while True:
            if token in self.outputs.keys():
                output = self.outputs.pop(token)
                if isinstance(output, str):
                    return output
                else:
                    return output[line]
            else:
                self.__internal_get_output_from_queue()

    def add_input(self, data, token=None):
        r"""Takes a token and an integer-data. The token specifies the input-request to provide 
        the given data to the correct request."""
        if token == None:
            while self.counter in self.used:
                self.counter += 1
            token = self.counter

        if isinstance(data,int):
            self.used.append(token)
            self.__internal_write_input_to_queue({token: str(data)})
        else:
            raise IOError("Input is not of type int!")
    
    def prepare_input_file(self, data):
        r"""Takes a list of input-\verb+data+. Prepares the private input-file for usage and
        copies the result to the correct folder."""      
        os.chdir(self.main_dir)
        
        filename = "gfp_vals"
        executable = "./gen_input_fp.x"
        
        
        if self.config["f2n"]:
            filename = "gf2n_vals"
            executable = "./gen_input_f2n.x"
        
        file = open(filename + ".in", "w")
        file.write(str(len(data)))
        for input in data:
            file.write(" " + str(input))
        file.close()
        
        p = subprocess.Popen(executable)
        p.wait()
        
        shutil.copyfile(filename + ".out", self.main_dir + "/Player-Data/Private-Input-" + str(self.config['player']))
        
        os.chdir(self.lib_dir)
    
    def wait(self):
        r'''Wait until execution of MPCProgram terminates.'''
        self.mpc.join()
    
    def terminate(self):
        if self.mpc.is_alive():
            self.mpc.terminate()