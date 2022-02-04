Other Components Callback Methods
=================================

Besides the :meth:`select_menu_callback<tungsten.Components.select_menu_callback>` 
and :meth:`button_callback<tungsten.Components.button_callback>` there are more callbacks 
that can be subclassed to add more custom functionality to your components.

Timeout Callback
----------------

One of the :class:`tungsten.Components` 's parameters is :attr:`timeout`, 
it is an integer that represents the amount of seconds the components can be without interaction 
before the :meth:`timeout_callback<tungsten.Components.timeout_callback>` method is called. 
The timer is restarted as soon as the components receive an interaction.

By default the :attr:`timeout` parameter will be set 
to 60 seconds and the :meth:`timeout_callback<tungsten.Components.timeout_callback>` 
will edit the message to show "Interaction Timed Out." along with it's components being removed.

As with other callbacks, it is possible to change it's behaviour by subclassing it.

**Example:**

.. code-block:: python

    async def timeout_callback(self) -> None:
        self.disable_components() 
        await self.edit_msg(f"Custom Timed Out", components = self.build())

This new custom :meth:`timeout_callback<tungsten.Components.timeout_callback>` method will disable it's components and update the contents of the message.


Not Allowed ID Callback
-----------------------

Another parameter in :class:`tungsten.Components` that can bring more functionality is :attr:`allowed_ids`, 
it is a list of allowed user IDs (:obj:`hikari.Snowflake<hikari.snowflakes.Snowflake>`) that can click the components in the message
without the :meth:`not_allowed_id_callback<tungsten.Components.not_allowed_id_callback>` triggering.

By default the :attr:`allowed_ids` parameter will be set to :obj:`None` which allows anyone from clicking 
the components and the :meth:`not_allowed_id_callback<tungsten.Components.not_allowed_id_callback>` will 
send a ephemeral response saying "You're not allowed to interact with this component." to whoever clicks 
it and is not in the :attr:`allowed_ids` list.

As with other callbacks, it is possible to change it's behaviour by subclassing it.

**Example:**

.. code-block:: python

    async def not_allowed_id_callback(self, event: hikari.InteractionCreateEvent) -> None:
        await self.ctx.respond("This interaction is not yours to click [This is a subclassed method]", flags = 64)

.. note::
    * Neither the :meth:`button_callback<tungsten.Components.button_callback>` nor the :meth:`select_menu_callback<tungsten.Components.select_menu_callback>` will be called if the :meth:`timeout_callback<tungsten.Components.timeout_callback>` is called.

Clicks Until Deactivate Callback
--------------------------------

Finally, yet another parameter in :class:`tungsten.Components` that can further customize your components 
is :attr:`clicks_until_deactivate`, it is an integer which represents the number of clicks that the components 
can receive before the :meth:`clicks_until_deactivate_callback<tungsten.Components.clicks_until_deactivate_callback>` is called.

By default the :attr:`clicks_until_deactivate` parameter will be set to 0 which allows any amount of clicks  
and the :meth:`clicks_until_deactivate_callback<tungsten.Components.clicks_until_deactivate_callback>` only disables the components.

As with other callbacks, it is possible to change it's behaviour by subclassing it.

**Example:**

.. code-block:: python

    async def clicks_until_deactivate_callback(self) -> None:
        await self.edit_msg(content = self.message.content, components= [])

.. note::
    * While the buttons are running, the variable :attr:`message` will return the :obj:`hikari.messages.Message` which the components are attached to.
    * This callback method does not need to necessarily disable the components, but the buttons will be deactivated after the callback is run.

