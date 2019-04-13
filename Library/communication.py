'''
(C) 2017 Malte Kruse. See License.txt.
'''
import os, pexpect, multiprocessing

def start_mpc(dir, config, program, input_queue, output_queue):  
    r'''Manage the running MPC process. That means: provide inputs and receive outputs.'''   
    os.chdir(dir)
    inputs = {}
    counter = 0
    cmd = "./Player-Online.x -pn " + str(config['port']) + " -h " + str(config['hostname']) + " " + str(config['player']) + " " + program
    p = pexpect.spawn(cmd, timeout=None)
    for line in p:
        string = __internal_byte_to_string(line)            
        if __internal_is_input(config['player'], string):
            while True:
                if counter in inputs.keys():
                    p.sendline(__internal_string_to_byte(str(inputs[counter])))
                    counter += 1
                    break;
                else:
                    inputs = __internal_get_input_from_queue(input_queue, inputs)
                  
        if __internal_is_output(config['player'], string):
            token = __internal_get_token(config['player'], string)
            obj = {token : ''}
            string = __internal_byte_to_string(p.readline())
            index = 0
            while __internal_is_output(config['player'], string, True):
                obj[token] = string
                index += 1
                string = __internal_byte_to_string(p.readline())
            __internal_write_output_to_queue(output_queue, obj)

def __internal_write_output_to_queue(output_queue, obj):
    r'''Used by subprocess managing the MPC. The process can always write output to the queue.'''
    output_queue.put(obj)
        
def __internal_get_input_from_queue(input_queue, inputs):
    r'''Receive all Elements passed to the input queue. 

    If input queue is empty, wait until elements are passed to the queue.'''
    input = input_queue.get();
    inputs.update(input)
            
    return inputs

def __internal_byte_to_string(bytes):
    r'''Translate byte-string to string'''
    return bytes.decode("utf-8").strip().replace('\r','')

def __internal_string_to_byte(string):
    r'''Translate string to byte-string'''
    return string.encode("utf-8")
    
def __internal_is_output(player, string, parse=False):
    r'''If \verb+parse+ = False: checks whether the given \verb+line+ indicates the start of user output or not.
    If \verb+parse+ = True: checks whether the given \verb+line+ indicates the end of user output or not. Used 
    for parsing multiline output between the tags.'''
    if string.startswith("#out_p%03i_" % (player)):
        return True
    if string.endswith("_p%03i_out#" % (player)):
        return False
    return parse   

def __internal_is_input(player, line):
    r'''Checks whether the line is an input-request for the current player or not.'''
    return line == "#in_p%03i" % (player)

def __internal_get_token(player, string):
    r'''Extracts the user specified token from the output-tag.'''
    return string[len("#out_p%03i_" % (player)):]