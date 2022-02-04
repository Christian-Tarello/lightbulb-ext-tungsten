.. _getting-started:

Getting Started
===============

In order to attach functioning components to a message it is necessary to subclass :class:`tungsten.Components`, 
by doing so potentially subclassing the :doc:`callback methods<guides/other-callbacks>` that are provided as 
a framework for organizing functionality.

.. note::
    This library is dependent on Hikari and Lightbulb, make sure both are up to date with this library.

Button Groups
-------------

Functioning button groups consist of two things:
    * A :class:`tungsten.ButtonGroup` instance provided with a list of lists with :class:`tungsten.Button` instances.
    * A subclassed :meth:`button_callback<tungsten.Components.button_callback>` in a :class:`tungsten.Components` subclass.

The :class:`tungsten.ButtonGroup` instance will be used to contain and modify the buttons, while the :meth:`button_callback<tungsten.Components.button_callback>`
is called everytime any of the buttons in the message are clicked.

.. note::
    * When subclassing callbacks such as the :meth:`button_callback<tungsten.Components.button_callback>`, they must have the same name and parameters as the ones in the parent class.


**Simple Color Changing**

.. code-block:: python

    from lightbulb.ext import tungsten

    class RainbowButtons(tungsten.Components):
        def __init__(self, *args, **kwargs):
            #Define a list of lists with tungsten.Button objects, representing a list of button rows
            button_rows = [
                            [
                            tungsten.Button("Rainbow", hikari.ButtonStyle.PRIMARY),
                            tungsten.Button("Rainbow", hikari.ButtonStyle.PRIMARY),
                            tungsten.Button("Rainbow", hikari.ButtonStyle.PRIMARY)
                            ],
                        ]
            #Set the variable "button_group" to an instance of the tungsten.ButtonGroup provided
            #with the list of button rows
            kwargs["button_group"] = tungsten.ButtonGroup(button_rows)
            #Run the __init__ method of the parent class
            super().__init__(*args, **kwargs)

        #The parameters on this method are referencing the button that was clicked.
        async def button_callback(
            self,
            button: tungsten.Button, 
            x: int, 
            y: int, 
            interaction: hikari.ComponentInteraction
            ) -> None:

            #Define the cycle of styles for the buttons to loop in
            color_cycle = {
                hikari.ButtonStyle.PRIMARY: hikari.ButtonStyle.SUCCESS,
                hikari.ButtonStyle.SUCCESS: hikari.ButtonStyle.SECONDARY,
                hikari.ButtonStyle.SECONDARY: hikari.ButtonStyle.DANGER,
                hikari.ButtonStyle.DANGER: hikari.ButtonStyle.PRIMARY
            }
            #Edit the button's style at the given coordinates 
            self.button_group.edit_button(x, y, style = color_cycle[button.style])
            #Edit the message updating the components using the build method
            await self.edit_msg(f"{button.style.name}", components = self.build())

    @bot.command #This assumes bot is an instance of lightbulb.BotApp
    @lightbulb.command("rainbow", "Produce three magic buttons.")
    @lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
    async def rainbow_command(ctx: lightbulb.Context) -> None:
        #Create an instance of RainbowButtons
        buttons = RainbowButtons(ctx)
        #Send the message with the components
        resp = await ctx.respond(f"Rainbow", components = buttons.build())
        #Run the components
        await buttons.run(resp)

When any of the three buttons is clicked it will change color and update the content of it's message.

.. note::

    * A button row shall not contain more than five buttons.
    * There shall be no more than 5 rows or more than 25 buttons in a :class:`tungsten.ButtonGroup`.
    * There is an easier way of predefining button appearances, check it out :doc:`here<guides/buttonstates>`.


Select Menus
------------

Functioning select menus consist of two things:
    * A :class:`tungsten.SelectMenu` instance provided with a list of :class:`tungsten.Option` instances.
    * A subclassed :meth:`select_menu_callback<tungsten.Components.select_menu_callback>` in a :class:`tungsten.Components` subclass.

The :class:`tungsten.SelectMenu` instance will be used to contain and modify the options, while the :meth:`select_menu_callback<tungsten.Components.select_menu_callback>`
is called everytime any of the options of the select menu in the message are clicked.

.. note::
    * When subclassing callbacks such as the :meth:`select_menu_callback<tungsten.Components.select_menu_callback>`, they must have the same name and parameters as the ones in the parent class.

**Simple Food Select Menu**

.. code-block:: python

    class SpamMenu(tungsten.Components):
        def __init__(self, *args, **kwargs):
            #Define a list of tungsten.Option objects, representing a list of options
            select_menu = [
                tungsten.Option("Spam", "Canned Spam", "🥫"),
                tungsten.Option("Ham", "Slices of Ham"),
                tungsten.Option("Eggs", emoji="🍳"),
                ]

            #Set the variable "select_menu" to an instance of the tungsten.SelectMenu provided 
            #with the list of options
            kwargs["select_menu"] = tungsten.SelectMenu(
                "Select your breakfast",
                min_chosen=1,
                max_chosen=2,
                options = select_menu
                )
            #Run the __init__ method of the parent class
            super().__init__(*args, **kwargs)

        #The parameters on this method are referencing the option(s) that was/were clicked.
        async def select_menu_callback(
            self,
            options: t.List[tungsten.Option],
            indexes: t.List[int],
            interaction: hikari.ComponentInteraction
            ) -> None:

            #loop through the indexes of the options that were clicked
            for index in indexes:
                #Edit the description of the option at the given index
                self.select_menu.edit_option(index, description="Clicked!")


            food = " | ".join([option.label for option in options])

            #Edit the message updating the components using the build method
            await self.edit_msg(f"Food: {food}", components = self.build())
        
        @bot.command #This assumes bot is an instance of lightbulb.BotApp
        @lightbulb.command("spam", "Produce a breakfast menu.")
        @lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
        async def spam_command(ctx: lightbulb.Context) -> None:
            #Create an instance of SpamMenu
            menu = SpamMenu(ctx)
            #Send the message with the components
            resp = await ctx.respond(f"Food", components = menu.build())
            #Run the components
            await menu.run(resp)

When any of the three options is clicked it will change it's description and update the content of it's message.


.. note::
    * Options in the select menu will appear as ordered in the list.
    * A select menu will occupy a whole button row, so it's not possible to have more than 4 button rows and a select menu.