
Button Groups Explained
=======================

How are Button Groups structured?
---------------------------------

Button Groups(:class:`tungsten.ButtonGroup`) methods work by accessing an item from the :attr:`button_rows` using coordinates. 
This library does not allow setting a custom ID for buttons, instead the custom ID are coordinates.
The coordinates start at the first button with x:0; y:0 and end at the twenty fifth button with x:4; y:4.

If you're still confused, here's a visual representation using lists and strings:

.. code-block:: python

    [
        ['0;0', '1;0', '2;0', '3;0', '4;0'],
        ['0;1', '1;1', '2;1', '3;1', '4;1'],
        ['0;2', '1;2', '2;2', '3;2', '4;2'],
        ['0;3', '1;3', '2;3', '3;3', '4;3'],
        ['0;4', '1;4', '2;4', '3;4', '4;4'],
    ]

Methods
-------

Besides the :meth:`edit_button<tungsten.ButtonGroup.edit_button>` method used in the :ref:`Getting Started<getting-started>` section, 
there are more methods that can add more functionality to your :meth:`button_callback<tungsten.Components.button_callback>`.
You can find them :class:`here<tungsten.ButtonGroup>`.
