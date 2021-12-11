"""Defines an observable object.

When an object needs to trigger an action, an Observable instance can be
created and callbacks can be associated to it. These callbacks will be
triggered each time the "set" method will be called.
"""

# =========================================================================== #
#  SECTION: Imports                                                           #
# =========================================================================== #

# =========================================================================== #
#  SECTION: Class definitions                                                 #
# =========================================================================== #

class Observable(object):
    """Defines an observable object.

    When an object needs to trigger an action, an Observable instance can be
    created and callbacks can be associated to it. These callbacks will be
    triggered each time the "set" method will be called.
    """

    def __init__(self, initial_value=None):
        """Initialized the Observable instance with no callbacks.

        @type inital_value: Same type than the object being observed.
        @param inital_value: Initial value given to the object being observed.
        """
        self.data = initial_value
        self.callbacks = {}
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------

    def add_callback(self, func):
        """Add a callback to the callbacks list.

        Add a callback method to the callbacks list. All these callbacks will
        be triggered when the "set" method will be called.

        @type func: Function / method
        @param func: Function / method to be called when the callbacks are
                     triggered.
        """
        self.callbacks[func] = 1
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------

    def del_callback(self, func):
        """Remove a callback from the callbacks list.

        @type func: Function / method
        @param func: Function / method that should not be called anymore when
                     the callbacks are triggered.
        """
        del self.callbacks[func]
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------

    def do_callbacks(self):
        """Calling all functions / methods one after the other."""
        for func in self.callbacks:
            func(self.data)
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------

    def set(self, data=None):
        """Update the value of the observed object and triggers callbacks.

        @type data: Same type than the object being observed.
        @param data: New value for the object being observed.
        """
        self.data = data
        self.do_callbacks()
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------

    def get(self):
        """Get the value of the object being observed."""
        return self.data
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------

    def unset(self):
        """Set to "None" the value of the object being observed."""
        self.data = None
    # -------------------------------------------------------------------------
