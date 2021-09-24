# CryoCon 22C Temperature Controller


> Install with `python -m pip install cryocon-22c-controller`

## API

A CryoconController is a SCPI instrument and uses the [easy-scpi](https://pypi.org/project/easy-scpi/) package for means of communication. Thus, all the methods and properties of an `easy_scpi.Instrument` can be called. 

Channels can be referenced either by their given name or their letter.
All commands generate a response from the controller, so only queries are performed to keep command and response synched.

### Methods

**CryoconController( port, timeout, baud, backend, \*\*resource_params ):** Creates a new CryoconController instance.

**max_temperatrue( loop ):** Returns the maximum set point temperature of the given loop.

**channel_max_temperatrue( loop ):** Returns the maximum set point temperature of the loop controlling the given channel.

**temperature( channel ):** Returns the current temperature of the given channel

**get_channel_loop( channel ):** Returns the loop controlled by the given channel.

**get_range( loop ):** Gets the output range for the loop. Values are [ 'hi', 'mid', 'low' ].

**set_range( loop, range ):** Sets the ouput range for the loop. Range values are [ 'hi', 'mid', 'low' ].

**get_ouput( loop ):** Gets the power output of the loop as a fraction of the full range.

**set_point( channel ):** Returns the set point of the given channel.

**set_temperature( channel, temperature ):** Sets the set point of the controlling loop of the given channel.

**lock( lock ):** Locks or unlocks the front key pad.

**enable():** Engages the temperature controller.

**disable():** Stops the tempreature controller. 

**auto_adjust_range( low_threshold, high_threshold, channles ):** Automatically adjusts the power range.

### Properties

**channels:** A dictionary of aliases of the channels.

**channel_names:** A dictionary of given name of the channels.

**loops:** A dictionary of loop:input source pairs.

**max_temps:** A dictionary of maximum set point temperatures for each loop.

**units:** A dictionary of units for each channel.

**enabled:** Returns whether the temperature controller is currently engaged.


### Example
~~~python
# import package
import cryocon_22c_controller as cc 

# Create a controller
cryo = cc.CryoconController( <port> )

# Connect to the controller
cryo.connect()

# Check if controller is connected (inherited from easy_scpi.Instrument)
cryo.is_connected

# Get channel names
cryo.channels

# Read the current set point temperature of channel a
cryo.set_point( 'a' )

# Set the desired temperature set point on channel b
cryo.set_temperature( 'b', 100 )

# Enable controller
cryo.enable()

# Disable controller
cryo.disable()
~~~