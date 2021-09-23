#!/usr/bin/env python
# coding: utf-8

# --- CryoCon Temperature Controller
# For use with a CryoCon 22C Temperature Controller

import easy_scpi as scpi


class CryoconController( scpi.Instrument ):
    """
    Represents a CryoCon 22C Temperature Controller

    Arbitrary SCPI commands can be performed
    treating the hieracrchy of the command as attributes.

    To read an property:  inst.p1.p2.p3()
    To call a function:   inst.p1.p2( 'value' )
    To execute a command: inst.p1.p2.p3( '' )
    """

    # --- methods ---

    def __init__(
        self,
        port = None,
        timeout = 10,
        baud = 9600,
        backend = '@py',
        **resource_params
    ):
        """
        Initializes an instance of the controller.

        :param port: The port associated to the hardware. [Default: None]
        :param timeout: Communication timeout in seconds. [Default: 10]
        :param baud: The hardware baudrate. [Default: 9600]
        :param backend: VISA backend to use. 
            See https://pyvisa.readthedocs.io/en/latest/introduction/getting.html#backend for more info.
            [Default: '@py']
        :param **resource_params: Arguments sent to the resource upon connection.
            See https://pypi.org/project/easy-scpi/ for more info.
        """
        scpi.Instrument.__init__(
            self,
            port = port,
            timeout = timeout* 1000,
            read_termination = '\r\n',
            write_termination = '\r\n',
            backend = backend
        )

        self.__channels = {}
        self.__channel_names = {}
        self.__loops = None
        self.__max_temps = None
        self.__units = None


    def connect( self ):
        super().connect()
        self.__channels = {
            # canonical channel names
            'a': [ 'cha' ],
            'b': [ 'chb' ]
        }
        self.__initialize_channel_names()  # user channel names

        self.__loops = self.__initialize_loop_sources()
        self.__units = self.__initialize_units()
        self.__max_temps = self.__initialize_max_temps()

        # lock keypad, turn remote LED on
        self.lock( True )


    def disconnect( self ):
        self.lock( False )
        super().disconnect()


    def __add_name_to_channel( self, channel, name ):
        """
        Adds an assoicated name to the channel.

        :param channel: The cahnnel to associate to.
        :param name: The new name of the channel.
        """
        name = name.strip().lower()
        self.channels[ channel ].append( name )


    def __initialize_channel_names( self ):
        """
        Gets the user channel name of each channel.
        """
        for chan in self.channels:
            name = self.channel_name( chan )
            self.__channel_names[ chan ] = name
            self.__add_name_to_channel( chan, name )



    def __initialize_loop_sources( self ):
        """
        Returns the source for each loop.

        :returns: A dictionary of loop:channel source pairs.
        """
        loops = { '1': None, '2': None, '3': None, '4': None }
        for loop in loops:
            source = self.query( 'loop {}:source?'.format( loop ) )
            loops[ loop ] = source.lower()

        return loops


    def __initialize_max_temps( self ):
        """
        Get the maximum set point temperature for each loop.

        :returns: A dictionary of loop:temperature pairs.
        """
        temps = { '1': None, '2': None, '3': None, '4': None }
        for loop in temps:
            ch = self.get_channel_by_name( self.loops[ loop ] )
            units = self.units[ ch ]

            temp = self.max_temperature( loop )
            temps[ loop ] = self.temp2float( temp, ch )

        return temps


    def __initialize_units( self ):
        """
        Gets the units for each input channel.

        :returns: A dictionary channel:unit pairs
        """
        units = { 'a': None, 'b': None }
        for ch in units:
            units[ ch ] = self.query( 'input {}:units?'.format( ch ) )

        return units


    def get_channel_by_name( self, name ):
        """
        Returns the canonical channel name of the given user channel name.

        :param name: A name describing the desired channel.
        :returns: The canonical channel name ('a' or 'b') or None if no match.
        """
        name = name.strip().lower()

        for channel, c_names in self.channels.items():
            if ( name == channel ) or ( name in c_names ):
                return channel

        # no match
        return None


    def channel_name( self, channel ):
        name = self.query( 'input {}:name?'.format( channel ) )
        return name.strip()


    def get_channel_loop( self, channel ):
        """
        Returns the loop controlled by the given channel.

        :param channel: The name of the channel to investigate.
        :returns: The controlled loop.
        """
        channel = self.get_channel_by_name( channel )

        for loop in [ '1', '2' ]:
            # loops 1 and 2 are controlled
            source = self.loops[ loop ]
            source = self.get_channel_by_name( source )
            if source == channel:
                return loop

        # loop not found
        return None


    @property
    def channels( self ):
        return self.__channels


    @property
    def channel_names( self ):
        return self.__channel_names


    @property
    def loops( self ):
        return self.__loops


    @property
    def max_temps( self ):
        return self.__max_temps


    @property
    def units( self ):
        return self.__units


    @property
    def enabled( self ):
        """
        Returns whether to controller is engaged or not.

        :returns: Boolean
        """
        resp = self.control()
        resp = resp.strip().lower()

        return ( resp == 'on' )


    def get_range( self, loop ):
        """
        Returns the range of the given loop.

        :param loop: The loop to examine.
        :returns: The range of the loop.
            Values are [ 'HI', 'MID', 'LOW' ]
        """
        rng = self.query( 'loop {}:range?'.format( loop ) )
        return rng.lower().strip()


    def set_range( self, loop, rng ):
        """
        Sets the range for the given loop.

        :param loop: The loop to modify.
        :param rng: The range to set.
            Values are [ 'hi', 'mid', 'low' ]
        """
        self.query( 'loop {}:range {}'.format( loop, rng ) )


    def get_output( self, loop ):
        """
        Gets the output power of the given loop as a percent of the full range.

        :param loop: The loop to examine.
        :returns: The fraction of the full range output power being applied.
        """
        pwr = self.query( 'loop {}:outpwr?'.format( loop ) )
        pwr = float( pwr )
        pwr /= 100

        return pwr


    def max_temperature( self, loop ):
        """
        Returns the maximum set point temperature for the given loop.

        :param loop: The loop to examine.
        :returns: The maximum set point of the loop.
        """
        return self.query( 'loop {}:maxset?'.format( loop ) )


    def channel_max_temperature( self, channel ):
        """
        Returns the maximum set point temperature for the given channel.

        :param channel: The channel to examine.
        :returns: The maximum set point of the channel.
        """
        loop = self.get_channel_loop( channel )
        if loop is None:
            return None

        return self.max_temps[ loop ]


    def temperature( self, channel ):
        """
        Returns the current temperature of the given channel.

        :param channel: The channel to set the temperature of.
            Valid values are [ 'a', 'A', 'b', 'B' ] or the channel name.
        :returns: The current temperature of teh channel.
        """
        channel = self.get_channel_by_name( channel )
        temp = self.query( 'input? {}'.format( channel ) )

        return float( temp )


    def set_point( self, channel ):
        """
        Returns the current set point for the given channel name.

        :param channel: The channel to examine.
        :returns: The set point of the loop associated to the channel.
        """
        loop = self.get_channel_loop( channel )

        if loop is None:
            # No loop found corresponding to channel
            return None

        setpt = self.query( 'loop {}:setpt?'.format( loop ) )

        return self.temp2float( setpt, channel )


    def set_temperature( self, channel, temperature ):
        """
        Set the set point temperature of the given channel.

        :param channel: The channel to set the temperature of.
        :param temperature: The nwe set point temperature.
        """
        loop = self.get_channel_loop( channel )
        max_temp = self.max_temps[ loop ]

        if temperature > max_temp:
            raise RuntimeError( 'Temperature is above maximum.' )

        self.query( 'loop {}:setpt {}'.format( loop, temperature ) )


    def enable( self ):
        """
        Engages control of the controller.
        """
        self.query( 'control' )

    def disable( self ):
        """
        Disable the temperature controller.
        """
        self.query( 'stop' )


    def lock( self, lock ):
        """
        Lock or unlocks teh front keypad.

        :param lock: A boolean of whether to lock (True) or unlock (False) teh keypad.
        """
        lock = 'on' if lock else 'off'
        self.query( 'system:lock {}'.format( lock ) )


    def temp2float( self, temp, channel ):
        """
        Converts a temeprature from a given channel to a float.
        Removes units from number part.

        :param temp: The temperature string.
        :param channel: Channel the temperature was acquired from.
        :returns:Float value of the temperature string.
        """
        channel = self.get_channel_by_name( channel )
        temp = temp.replace( self.units[ channel ], '' )
        return float( temp )


    def auto_adjust_range( self, threshold_low  = 0.09, threshold_high = 0.95, channels = None ):
        """
        Automatically adjusts the range of the loop.

        :param threshold_low: Lower power threshold to switch range.
            Given as fraction of total power. [Default: 0.09]
        :param threshold_high: Upper power threshold to switch range.
            Given as fraction of total power. [Default: 0.95]
        :param channels: List of channels to control, or None to control all. [Default: None]
        """

        def change_range( curr, change ):
            """
            Gets the range relative to the given differing by change.

            :param curr: Name of current range.
                Values in [ 'low', 'mid', 'high' ].
            :param change: Step to attempt change.
            :returns: Name of new range given the current position and change, or None if change goes outside of bounds.
                Values in [ 'low', 'mid', 'high', None ]
            """
            ranges = [ 'low', 'mid', 'hi' ]
            pos = ranges.index( curr )
            pos += change

            if ( pos < 0 ) or ( pos >= len( ranges ) ):
                # index out of bounds
                return None

            return ranges[ pos ]


        if channels is None:
            channels = self.channels.keys()

        for ch in channels:
            loop = self.inst.get_channel_loop( ch )
            if loop is None:
                continue

            output = self.inst.get_output( loop )
            rng = self.inst.get_range( loop )
            new_rng = None
            if output < threshold_low:
                new_rng = change_range( rng, -1 )

            elif output > threshold_high:
                new_rng = change_range( rng, 1 )

            if new_rng is not None:
                 self.inst.set_range( loop, new_rng )
