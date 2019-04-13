# SPDZ-2-Library-ReactiveMPC
The goal of this library is to provide reactive secure multi-party computations (MPC) for python programs. This library enables to run multiple MPCs concurrently from within a python program. Therefore communication between MPC and the python program is realised by using stdin and stdout of the processes. As proof of concept the game <a href="https://en.wikipedia.org/wiki/Mastermind_(board_game)">Mastermind</a> was implemented using this library. There is also a second version, which only uses the original SPDZ-2 framework to show the gain of using the library.<br/><br/>This library was developed as part of my Bacherlor Thesis.

&copy; 2017, Malte Kruse. See License.txt.

<b>Note:</b><br />
The files in the directories <i>Compiler</i> and <i>Processor</i> are modified versions of the files used in the original <a href="https://github.com/bristolcrypto/SPDZ-2">SPDZ-2</a>-project and are copyrighted by &copy; 2016, The University of Bristol. See also License_SPDZ2.txt.

## Requirements
The Requirements for using the library, are listed below:
- SPDZ-2 (commit <a href="https://github.com/bristolcrypto/SPDZ-2/tree/1ed6ff65be49489a26cce1b9e100c7abeb9f1957">1ed6ff6</a>), version linked as submodule
- pexpect <a href="https://github.com/pexpect/pexpect/releases/tag/4.2.1">v4.2.1</a>

Running the MastermindGUI-Example additionally requires:

- Python 3.0 or higher
- tkinter for Python

## Installation
To install the Library, you have to follow these steps:

<ol>
<li>Clone this git repository and download the SPDZ-2 submodule. Therefore type:
<br />

<code>git clone --recurse-submodules https://github.com/iSecurus/reactiveMPC.git</code>

<b>Note:</b> Should the download of SimpleOT fail, it is not problematic, because the Offline-Phase is not necessary to run SPDZ-2. <b>Also the Offline-Phase of SPDZ-2 is not supported by this library</b>. If SimpleOT is still needed, you could clone it directly from its <a href="https://github.com/pascholl/SimpleOT/tree/52b43a250922fb45f0bfff73ba2f9b9a11c1784c">repository</a> as follows:
<br />

```
git clone https://github.com/pascholl/SimpleOT.git
cd SimpleOT
git checkout 52b43a2
```
</li>
<li>
<code>cd SPDZ-2-Library-ReactiveMPC</code>
</li>
<br />
<li>
Copy or move all files and directories listed below into the SPDZ-2 directory. Make sure that you override the existing files.
<br />
<br />
<pre>
SPDZ-2-Library-ReactiveMPC
|-- <b><i>Compiler/</i></b>
|-- <b><i>Library/</i></b>
|-- <b><i>Processor/</i></b>
|-- <b><i>Programs/</i></b>
|-- <b><i>__init__.py</i></b>
</pre>
</li>
<li> 
Compile and install the prepared version of SPDZ-2 as shown <a hred="https://github.com/bristolcrypto/SPDZ-2">here</a>. 
</li>
</ol>

## Running the example
To run the examples, you have to make sure, that Python 3.0 or higher and tkinter are installed. Open up a shell and navigate to the root directory of SPDZ-2. Then perform the following steps:

<ol>
<li>
<code>cd Programs/Source/MastermindGUI</code>
</li>
<br/>
<li>
Create an symbolic link named <b>SPDZ2</b>, pointing to the root-directory of SPDZ-2:<br/>
</br>
<code>ln -s ../../../ SPDZ2</code>
</li>
<br/>
<li>
Modify <code>port</code>, <code>hostname</code> and other configurations as needed in <code>codebreaker.py</code> and <code>codemaker.py</code>.
</li>
<br/>
<li>
Open two shells. In the first one run:<br />
<br/>
<code>python3 codemaker.py</code>

and in the second one:

<code>python3 codebreaker.py</code>
</li>

</ol>

## Python API
To embed a MPC into your python program add `import Path.to.Library.SPDZ` to the list of imports. Than create an instance of `MPCProgram()` as shown in the table below. The table also lists all other functions, which can be called on the MPCProgram.


   | Method | Default values | Description |
   | :--- | :--- | :--- |
   | MPCProgram(program, player, <br/>max_player, port, hostname, f2n) | player=0<br/>max_player=2<br/>port=5000<br/>hostname='localhost'<br/>f2n=false | Initializes the MPC program to be computed by this framework. More than one MPC program could be defined and run concurrently. |
   | run() |   | Runs MPCProgram.  |
   | clear() |   | Clears all data of the previous run of MPCProgram. Needs to be invoked before every rerun of MPCProgram.  |
   |configure(key, config) |   | (Re)configures the specified server and connection settings set within the constructor MPCProgram.  |
   | get_private_output() |   | Reads out the private output file of the caller.  |
   | get_public_output() |   |  Reads out the public output file of the caller. |
   | get_output(token, line) | line=0 | Reads out the stdout, waiting for an output message taged with the specified token. The token can be self defined by the user. If a multiline output is expected, the line to be read can be specified by the line number. The output read by this method will be saved for later use within the MPCProgram. |
   | pop_output(token, line) | line=0 | Same as get_output(token, line). Instead of saving the output for later use within MPCProgram, it will be deleted. Enables reuse of the same Token inside an MPCProgram. |
   | add_input(data, token) | token=None | Inputs the given data via stdin to MPCProgram. If no token is defined, it will be considered to be the next free token, expected by the program. To prepare inputs for later, a numeric token x can be defined. You have to consider the token as "the x-th input the MPCProgram expected". Reuse of an token leads to overriding the previous value.  |
   | prepare_input_file(data) |   | Accepts a list of numeric input data and uses it to prepare the SPDZ input file for use by the MPCProgram.  |
   | wait() |   | Wait for the MPCProgram to complete, before continuing to run the python program. |
   | terminate() |   | Stops MPCProgram execution.  |
   
## SPDZ API
The table below shows the additional functions, you have to use within your SPDZ program, to communicate with the python program via stdin/stdout. Both new and modified functions are listed.

  | Method | Default values | Description |
  | :--- | :--- | :--- |
  | print_ln_to(player,<br/>s, *args) | player=0,<br/>s='' | Prints the given string only to the given player. Extended version of `print_ln()`, which was made for debug-reasons to print only to player 0. |
  | get_input_from(player) |   | Modified version of the former `get_input_from(player)` method. Additionally prints out a token, signaling the MPC waits for an user specific input by the specified player. The MPC will be paused until the requested input was delivered. The requested inputs will be automatically sequenced per player from 0, 1, 2 to number of inputs needed.<br/><br/>Input can be commited with `add_input(data, token)` within the python program at any time. Given the knowledge of the inputs needed by the MPC, a player can use the specific token from 0, 1, 2 to number of inputs, to prepare inputs for later usage.|
  | print_output_to(player,<br/>token, s, *args) | player=0,<br/>token='',<br/>s=''  | Prints output of a computation to a given player using a player-defined token. The token is used to realize the communication between MPC and python program. Outputs will be read in the python program and stored for later usage. Only the last known value for a token will be stored, this could lead to lost updates when not read in between. Multiline outputs are possible, too.<br/><br/>Uses `print_ln_to(player)` and can be read multiple times with `get_output(token, line)` or once with `pop_output(token, line)`. |
   
