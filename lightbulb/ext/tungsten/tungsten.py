# -*- coding: utf-8 -*-
# Copyright © Christian-Tarello 2022-present
#
# This file is part of Tungsten.
#
# Tungsten is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Tungsten is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Tungsten. If not, see <https://www.gnu.org/licenses/>.

from __future__ import annotations

__all__ = [
    "ButtonState",
    "Button",
    "ButtonGroup",
    "Option",
    "SelectMenu",
    "Components",
]

import asyncio
from dataclasses import dataclass, field
import typing as t

import hikari

if t.TYPE_CHECKING:
    import lightbulb


@dataclass
class ButtonState:
    """
    Dataclass that represents a state for a representation of a Discord Button.
    Button States are really just a way to easily change the appearance of a button
    by predefining states.

    Args:
        label (:obj:`str` | :obj:`int`): The label of the button.
        style (:obj:`int` | :obj:`hikari.ButtonStyle<hikari.messages.ButtonStyle>`): The type of style this button state uses.
        emoji (:obj:`hikari.Snowflakeish<hikari.snowflakes.Snowflake>` | :obj:`hikari.Emoji<hikari.emojis.Emoji>` | :obj:`str`): A emoji that is shown along with the label.

    """

    label: t.Union[str, int, None] = None
    style: t.Union[int, hikari.ButtonStyle, None] = None
    emoji: t.Union[hikari.Snowflakeish, hikari.Emoji, str, None] = None


@dataclass
class Button:
    """
    Dataclass that represents a Discord Button.

    Args:
        label (:obj:`str` | :obj:`int`): The label of the button.
        style (:obj:`int` | :obj:`hikari.ButtonStyle<hikari.messages.ButtonStyle>`): The type of style this button uses.
        emoji (:obj:`hikari.Snowflakeish<hikari.snowflakes.Snowflake>` | :obj:`hikari.Emoji<hikari.emojis.Emoji>` | :obj:`str`): A emoji that is shown along with the label.
        is_disabled (:obj:`bool`): Whether this button can be clicked or not.
        url (:obj:`str`): Url for the button provided it is intended to be a link button. Link buttons will not trigger a callback when clicked.
        state (:obj:`typing.Hashable`): If the button has button states, this is where the hashable for the current state goes.
        button_states (Dict[:obj:`typing.Hashable`, :obj:`ButtonState`]): A dictionary mapping to :obj:`ButtonState` objects.
    """

    label: t.Union[str, int, None] = None
    style: t.Union[int, hikari.ButtonStyle, None] = None
    emoji: t.Union[hikari.Snowflakeish, hikari.Emoji, str, None] = None
    is_disabled: bool = False
    url: t.Union[str, None] = None
    state: t.Optional[t.Hashable] = None
    button_states: t.Optional[t.Dict[t.Hashable, ButtonState]] = None

    _label: t.Union[str, int, None] = field(init=False, repr=False)
    _style: t.Union[int, hikari.ButtonStyle, None] = field(init=False, repr=False)
    _emoji: t.Union[hikari.Snowflakeish, hikari.Emoji, str, None] = field(
        init=False, repr=False
    )
    _x: int = field(init=False, repr=False)
    _y: int = field(init=False, repr=False)

    @property
    def coordinates(self) -> t.Tuple[int, int]:
        return (self._x, self._y)

    @coordinates.setter
    def coordinates(self, value: t.Tuple[int, int]):
        assert isinstance(value, tuple) and len(value) == 2
        self._x = value[0]
        self._y = value[1]

    @property
    def style(
        self,
    ) -> t.Union[
        int, hikari.ButtonStyle, None
    ]:  # style changes according to the value of the cell
        if self.button_states:
            return getattr(self.button_states[self.state], "style", self._style)
        elif not isinstance(self._style, property):
            return self._style
        else:
            return None

    @style.setter
    def style(self, value: t.Union[int, hikari.ButtonStyle]) -> None:
        self._style = value

    @property
    def label(self) -> t.Union[str, int, None]:
        if self.button_states:
            return getattr(self.button_states[self.state], "label", self._label)
        elif not isinstance(self._label, property):
            return self._label
        else:
            return None

    @label.setter
    def label(self, value: t.Union[str, int]) -> None:
        self._label = value

    @property
    def emoji(self) -> t.Union[hikari.Snowflakeish, hikari.Emoji, str, None]:
        if self.button_states:
            return getattr(self.button_states[self.state], "emoji", self._emoji)
        elif not isinstance(self._emoji, property):
            return self._emoji
        else:
            return None

    @emoji.setter
    def emoji(self, value: t.Union[hikari.Snowflakeish, hikari.Emoji, str]) -> None:
        self._emoji = value


TButtonGroup = t.TypeVar("TButtonGroup", bound="ButtonGroup")


class ButtonGroup(object):
    """
    A class designed to contain and modify a List[List[:obj:`Button`]].

    In order to use it, an instance of this class has to be manually
    added as an argument to the constructor of a :obj:`Components` instance.

    Args:
        button_rows(List[List[:obj:`Button`]]): The List[List[:obj:`Button`]] meant to be contained and modified.
    """

    __slots__ = ("button_rows", "link_mapping")

    def __init__(
        self: TButtonGroup, button_rows: t.Optional[t.List[t.List[Button]]] = None
    ):
        self.button_rows = button_rows or [[], [], [], [], []]
        self.link_mapping: t.Dict = {}

    def add_button(
        self: TButtonGroup,
        button: Button,
        y: int = None,
        update_coordinates: bool = True,
    ) -> TButtonGroup:
        """
        Adds a button to the end of :attr:`button_rows`.
        Updating coordinates will set coordinates to the new button.
        It will fail if there's 25 buttons in :attr:`button_rows` already.
        Returns :obj:`self`, so chaining methods is possible.
        """
        if y or y == 0:
            if (x := len(self.button_rows[y])) < 5:
                coordinates = (x, y)
        else:
            for y, row in enumerate(self.button_rows):
                if (x := len(row)) < 5:
                    coordinates = (x, y)
                    break

        if update_coordinates:
            button.coordinates = coordinates

        self.button_rows[coordinates[1]].append(button)

        return self

    def overwrite_button(
        self: TButtonGroup,
        button: Button,
        x: int,
        y: int,
        update_coordinates: bool = True,
    ) -> TButtonGroup:
        """
        Overwrites a button at the given coordinates in :attr:`button_rows`.
        Updating coordinates will set the given coordinates to the new button.
        Returns :obj:`self`, so chaining methods is possible.
        """
        self.button_rows[y][x] = button
        if update_coordinates:
            self.button_rows[y][x].coordinates = (x, y)
        return self

    def edit_button(self: TButtonGroup, x: int, y: int, **kwargs) -> TButtonGroup:
        """
        Edits a button at the given coordinates in :attr:`button_rows` with the given arguments.
        Returns :obj:`self`, so chaining methods is possible.
        """
        button = self.button_rows[y][x]
        for k, v in kwargs.items():
            setattr(button, k, v)
        self.button_rows[y][x] = button
        return self

    def remove_button(
        self: TButtonGroup, x: int, y: int, update_coordinates: bool = True
    ) -> TButtonGroup:
        """
        Removes a button at the given coordinates in :attr:`button_rows`.
        Updating coordinates will substract 1 to the x coordinate of the buttons that follow the removed button in the row.
        Returns :obj:`self`, so chaining methods is possible.
        """
        if self.button_rows[y] and len(self.button_rows[y]) > 0:
            del self.button_rows[y][x]
            if update_coordinates:
                for button in self.button_rows[y]:
                    if button._x > x:
                        button._x -= 1
        return self

    def insert_button(
        self: TButtonGroup,
        button: Button,
        x: int,
        y: int,
        update_coordinates: bool = True,
    ) -> TButtonGroup:
        """
        Inserts a button at the given coordinates in :attr:`button_rows`.
        Updating coordinates will add 1 to the x coordinate of the buttons that follow the inserted button in the row.
        WARNING: It will not work if the row is already full.
        Returns :obj:`self`, so chaining methods is possible.
        """
        if len(self.button_rows[y]) < 5 and x < 5:
            button.coordinates = (x, y)
            self.button_rows[y].insert(x, button)
            if update_coordinates:
                for button in self.button_rows[y][x+1:]:
                    button._x += 1
        return self

    def switch_button_position(
        self: TButtonGroup,
        x: int,
        y: int,
        x2: int,
        y2: int,
        update_coordinates: bool = True,
    ) -> TButtonGroup:
        """
        Switches two buttons positions at the given coordinates in :attr:`button_rows`.
        Updating coordinates will switch the buttons coordinates too.
        Returns :obj:`self`, so chaining methods is possible.
        """
        button_one = self.button_rows[y][x]
        button_two = self.button_rows[y2][x2]
        self.overwrite_button(button_one, x2, y2, update_coordinates=update_coordinates)
        self.overwrite_button(button_two, x, y, update_coordinates=update_coordinates)
        return self

    def _build(
        self: TButtonGroup, ctx: lightbulb.context.Context
    ) -> t.List[hikari.api.ActionRowBuilder]:
        action_rows = []
        for y, row in enumerate(self.button_rows):
            if not row:
                continue
            action_row = ctx.app.rest.build_action_row()
            for x, button in enumerate(row):
                if not button.url:
                    button._x = x
                    button._y = y
                    button_component = action_row.add_button(
                        button.style, f"{button._x},{button._y}"
                    ).set_label(f"{button.label}")
                else:
                    # Running a button with links in it will make response return None
                    # IDK if this is my fault or hikari's fault
                    button_component = action_row.add_button(
                        hikari.ButtonStyle.LINK, button.url
                    ).set_label(f"{button.label}")
                    self.link_mapping[button.url] = (x, y)

                if button.emoji:
                    button_component.set_emoji(button.emoji)

                if button.is_disabled:
                    button_component.set_is_disabled(True)
                button_component.add_to_container()

            action_rows.append(action_row)  # adds the row to the list of rows
        return action_rows

    def disable_all_buttons(self: TButtonGroup):
        """
        Sets all buttons :attr:`is_disabled` attribute to True on :attr:`button_rows`.
        """
        for row in self.button_rows:
            for button in row:
                button.is_disabled = True


@dataclass
class Option:
    """
    Dataclass that represents a Discord Option from a select menu.

    Args:
        label (:obj:`str` | :obj:`int`): The label of the option.
        description (:obj:`str`): The description of the button.
        emoji (:obj:`hikari.Snowflakeish<hikari.snowflakes.Snowflake>` | :obj:`hikari.Emoji<hikari.emojis.Emoji>` | :obj:`str`): A emoji that is shown along with the label.
        is_default (:obj:`bool`): Whether this option should be selected by default.
    """

    label: t.Union[str, int]
    description: str = " "
    emoji: t.Union[hikari.Snowflakeish, hikari.Emoji, str, None] = None
    is_default: bool = False
    _index: t.Union[int, None] = field(init=False, repr=False)


TSelectMenu = t.TypeVar("TSelectMenu", bound="SelectMenu")


class SelectMenu(object):
    """
    A class designed to contain and modify a List[:obj:`Option`].

    In order to use it, an instance of this class has to be manually
    added as an argument to the constructor of a :obj:`Components` instance.

    The options will be displayed from bottom to top.

    Args:
        placeholder (:obj:`str`): The placeholder of the select menu.
        is_disabled (:obj:`bool`): Whether the select menu is disabled.
        min_chosen (:obj:`int`): The minimum amount of options which must be chosen for this menu.
        max_chosen (:obj:`int`): The maximum amount of options which can be chosen for this menu.
        custom_id (:obj:`str`): The custom ID of the select menu.
        options (List[:obj:`Option`]): A List[:obj:`Option`] meant to be contained and modified.

    """

    def __init__(
        self: TSelectMenu,
        placeholder: str,
        is_disabled: bool = False,
        min_chosen: int = 1,
        max_chosen: int = 1,
        custom_id: str = "select_menu",
        options: t.Optional[t.List[Option]] = None,
    ):

        self.placeholder = placeholder
        self.is_disabled = is_disabled
        self.min_chosen = min_chosen
        self.max_chosen = max_chosen
        self.custom_id = custom_id
        self.options = options or []

    def add_option(
        self: TSelectMenu, option: Option, update_indexes: bool = True
    ) -> TSelectMenu:
        """
        Adds an option to the end of :attr:`options`.
        Updating indexes will set the index to the new option.
        Returns :obj:`self`, so chaining methods is possible.
        """
        if update_indexes:
            option._index = len(self.options)
        self.options.append(option)
        return self

    def overwrite_option(
        self: TSelectMenu, option: Option, index: int, update_indexes: bool = True
    ) -> TSelectMenu:
        """
        Overwrites a option at the given index in :attr:`options`.
        Updating indexes will set the index to the new option.
        Returns :obj:`self`, so chaining methods is possible.
        """
        self.options[index] = option
        if update_indexes:
            self.options[index]._index = index
        return self

    def edit_option(self: TSelectMenu, index: int, **kwargs) -> TSelectMenu:
        """
        Edits an option at the given index in :attr:`options` with the given arguments.
        Returns :obj:`self`, so chaining methods is possible.
        """
        option = self.options[index]
        for k, v in kwargs.items():
            setattr(option, k, v)
        self.options[index] = option
        return self

    def remove_option(
        self: TSelectMenu, index: int, update_indexes: bool = True
    ) -> TSelectMenu:
        """
        Removes an option at the given index in :attr:`options`.
        Updating indexes will substract 1 to the index of the options that follow the removed option.
        Returns :obj:`self`, so chaining methods is possible.
        """
        del self.options[index]
        if update_indexes:
            for option in self.options[index:]:
                option._index -= 1
        return self

    def insert_option(
        self: TSelectMenu, option: Option, index: int, update_indexes: bool = True
    ) -> TSelectMenu:
        """
        Inserts an option at the given index in :attr:`options`.
        Updating indexes will add 1 to the index of the options that follow the removed option.
        Returns :obj:`self`, so chaining methods is possible.
        """
        option._index = index
        self.options.insert(index, option)
        if update_indexes:
            for option in self.options[index + 1 :]:
                option._index += 1
        return self

    def switch_option_position(
        self: TSelectMenu, index: int, index2: int, update_indexes: bool = True
    ) -> TSelectMenu:
        """
        Switches two options positions at the given coordinates in :attr:`options`.
        Updating indexes will switch the options indexes too.
        Returns :obj:`self`, so chaining methods is possible.
        """
        option_one = self.options[index]
        option_two = self.options[index2]
        self.overwrite_option(option_one, index2, update_indexes=update_indexes)
        self.overwrite_option(option_two, index, update_indexes=update_indexes)
        return self

    def _build(
        self, ctx: lightbulb.context.Context
    ) -> t.List[hikari.api.ActionRowBuilder]:
        action_row = ctx.app.rest.build_action_row()
        select_menu = action_row.add_select_menu(self.custom_id)
        select_menu.set_placeholder(self.placeholder)
        select_menu.set_min_values(self.min_chosen)
        select_menu.set_max_values(self.max_chosen)
        select_menu.set_is_disabled(self.is_disabled)

        for index, option in enumerate(self.options):
            option._index = index

            option_builder = select_menu.add_option(
                f"{option.label}", f"{option._index}"
            )
            option_builder.set_description(f"{option.description}")
            if option.emoji is not None:
                option_builder.set_emoji(option.emoji)
            option_builder.set_is_default(option.is_default)
            option_builder.add_to_menu()

        select_menu.add_to_container()

        return [
            action_row,
        ]

    def disable_all_options(self):
        """
        Sets this object's :attr:`is_disabled` attribute to True, thus setting to disable all options in the select menu.
        """
        self.is_disabled = True


class Components(object):
    """
    Base class for making a :obj:`Components` instance.

    This class is to be subclassed, potentially overwriting the following methods:
        - :meth:`button_callback<Components.button_callback>`

        - :meth:`select_menu_callback<Components.select_menu_callback>`

        - :meth:`timeout_callback<Components.timeout_callback>`

        - :meth:`not_allowed_id_callback<Components.not_allowed_id_callback>`

        - :meth:`clicks_until_deactivate_callback<Components.clicks_until_deactivate_callback>`

    The subclassed methods must have the same name and accept the same parameters.

    Args:
        context (:obj:`lightbulb.Context<lightbulb.context.base.Context>`): The :obj:`lightbulb.Context<lightbulb.context.base.Context>` to use.
        timeout (:obj:`float`): The timeout length in seconds.
        allowed_ids (List[:obj:`hikari.Snowflake<hikari.snowflakes.Snowflake>`]): List of ids allowed to click on the components. Setting this to :obj:`None` will allow anyone to click them.
        clicks_until_deactivate (:obj:`int`): The number of times it can be clicked before calling :meth:`clicks_until_deactivate_callback<Components.clicks_until_deactivate_callback>`. Set this to 0, if you don't want a click limit.
        button_group(:obj:`ButtonGroup`): The :obj:`ButtonGroup` to use.
        select_menu(:obj:`SelectMenu`): The :obj:`SelectMenu` to use.

    """

    def __init__(
        self,
        ctx: lightbulb.context.Context,
        timeout: int = 60,
        allowed_ids: t.Optional[t.List[hikari.Snowflakeish]] = None,
        clicks_until_deactivate: int = 0,
        button_group: t.Optional[ButtonGroup] = None,
        select_menu: t.Optional[SelectMenu] = None,
    ):

        self.ctx = ctx
        self.timeout_length = timeout
        self.allowed_ids = allowed_ids or []
        self.clicks_until_deactivate = clicks_until_deactivate
        self.button_group = button_group
        self.select_menu = select_menu
        self._is_disabled: bool = False
        self._clicks: int = 0

    async def button_callback(
        self, button: Button, x: int, y: int, interaction: hikari.ComponentInteraction
    ) -> None:
        """This method is a default placeholder meant to be overwritten in a subclass. Though it can be left as is if you wish."""
        pass

    async def select_menu_callback(
        self,
        options: t.List[Option],
        indexes: t.List[int],
        interaction: hikari.ComponentInteraction,
    ) -> None:
        """This method is a default placeholder meant to be overwritten in a subclass. Though it can be left as is if you wish."""
        pass

    async def timeout_callback(self) -> None:
        """This method is a default placeholder meant to be overwritten in a subclass. Though it can be left as is if you wish."""
        await self.edit_msg("Interaction Timed Out.", components=[])

    async def not_allowed_id_callback(
        self, event: hikari.InteractionCreateEvent
    ) -> None:
        """This method is a default placeholder meant to be overwritten in a subclass. Though it can be left as is if you wish."""
        await event.interaction.create_initial_response(
            hikari.ResponseType.MESSAGE_CREATE,
            "You're not allowed to interact with this component.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )

    async def clicks_until_deactivate_callback(self) -> None:
        """This method is a default placeholder meant to be overwritten in a subclass. Though it can be left as is if you wish."""
        self.disable_components()
        await self.edit_msg(content=self.message.content, components=self.build())

    async def _process_event(self, event: hikari.InteractionCreateEvent) -> None:
        """Processes the given :obj:`hikari.InteractionCreateEvent`."""

        assert isinstance(event.interaction, hikari.ComponentInteraction)

        if event.interaction.user.id not in self.allowed_ids and self.allowed_ids:
            return await self.not_allowed_id_callback(event)

        await event.interaction.create_initial_response(
            hikari.ResponseType.DEFERRED_MESSAGE_UPDATE,  # DEFERRED_MESSAGE_UPDATE acknowledges the interaction
        )

        if event.interaction.component_type == hikari.ComponentType.BUTTON:
            x, y = [int(i) for i in event.interaction.custom_id.split(",")]
            button = self.button_group.button_rows[y][x]
            await self.button_callback(button, x, y, event.interaction)

        elif event.interaction.component_type == hikari.ComponentType.SELECT_MENU:
            indexes = [int(index) for index in event.interaction.values]
            options = [self.select_menu.options[index] for index in indexes]
            await self.select_menu_callback(options, indexes, event.interaction)

        if self.clicks_until_deactivate:
            self._clicks += 1
            if self.clicks_until_deactivate == self._clicks:
                await self.clicks_until_deactivate_callback()
                self.deactivate_components()

    async def run(self, resp: lightbulb.ResponseProxy) -> None:
        """
        Run a :obj:`Components` loop binded to the message of the given :obj:`lightbulb.ResponseProxy<lightbulb.context.base.ResponseProxy>`.
        """

        assert self.button_group or self.select_menu
        # assert self.resp is not None
        # The response is equal to None if there's a link button, not sure why.
        # Everything still works with the response being equal to None, again not sure why.

        self.message = await resp.message()
        while True:
            try:
                event = await self.ctx.bot.wait_for(
                    hikari.InteractionCreateEvent,
                    timeout=self.timeout_length,
                    predicate=lambda e: isinstance(
                        e.interaction, hikari.ComponentInteraction
                    )
                    and e.interaction.message.id == self.message.id,
                )
            except asyncio.TimeoutError:
                await self.timeout_callback()
                break
            else:
                await self._process_event(event)
                if self._is_disabled:
                    break

    def build(self) -> t.List[hikari.api.ActionRowBuilder]:
        """
        Builds the :obj:`Components` components.
        Will skip building :obj:`SelectMenu` if there's five rows of buttons already.
        This function also automatically updates the components indexes and coordinates.

        Returns:
            List[:obj:`hikari.api.ActionRowBuilder<hikari.api.special_endpoints.ActionRowBuilder>`]
        """
        if (
            self.button_group
            and self.select_menu
            and not self.button_group.button_rows[4]
        ):
            button_action_row = self.button_group._build(self.ctx)
            select_menu_action_row = self.select_menu._build(self.ctx)
            button_action_row.extend(select_menu_action_row)
            return button_action_row

        elif self.button_group:
            button_action_row = self.button_group._build(self.ctx)
            return button_action_row

        else:
            select_menu_action_row = self.select_menu._build(self.ctx)
            return select_menu_action_row

    async def edit_msg(self, *args: t.Any, **kwargs: t.Any) -> None:
        """
        Edits the message binded to this instance of :obj:`Components`.

        Accepts any argument that can be passed to :meth:`hikari.messages.PartialMessage.edit`.
        """
        self.message = await self.message.edit(*args, **kwargs)

    def disable_components(self) -> None:
        """Sets the components to be disabled and deactivated, you still have build the components to update them"""
        if self.button_group:
            self.button_group.disable_all_buttons()
        if self.select_menu:
            self.select_menu.disable_all_options()
        self.deactivate_components()

    def deactivate_components(self) -> None:
        """If called, it deactivates the components as soon as a callback is done running."""
        self._is_disabled = True
