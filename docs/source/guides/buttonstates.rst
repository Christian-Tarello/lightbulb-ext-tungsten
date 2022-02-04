
Button States
=============

Using :class:`tungsten.ButtonState`, predefining button appearances becomes way easier. This object is a dataclass 
capable of storing a basic appearance of a button. :class:`tungsten.ButtonState` must be stored in a dictionary as 
values to keys identifying each state.

There are two parameters in :class:`tungsten.Button` that make this integration possible:
    * `state`
    * `button_states`

The :attr:`tungsten.Button.button_states` parameter is used to store the dictionary, while the :attr:`tungsten.Button.state` parameter is the key in the dictionary 
that defines which button state is currently active.

**Example:**

.. code-block:: python

    button_states = {
                    1: tungsten.ButtonState(label = "RED", style=hikari.ButtonStyle.DANGER, emoji="💣"),
                    2: tungsten.ButtonState(label="GREY", style=hikari.ButtonStyle.SECONDARY),
                    3: tungsten.ButtonState(label="GREEN", style=hikari.ButtonStyle.SUCCESS, emoji="👍"),
                    4: tungsten.ButtonState(label="BLURPLE", style=hikari.ButtonStyle.PRIMARY)
                }

    button_rows = [
                    [
                    tungsten.Button(state=2, button_states=button_states),
                    tungsten.Button(state=4, button_states=button_states),
                    tungsten.Button(state=2, button_states=button_states),
                    tungsten.Button(state=3, button_states=button_states),
                    ]
                ]

.. note::
    * A button that uses button states will always prioritize the :class:`tungsten.ButtonState` appearance over paramters such as :attr:`label`, :attr:`style` and :attr:`emoji`
