from aiogram import Router, F
from aiogram.filters import MagicData, invert_f
from aiogram.types import CallbackQuery
from asgiref.sync import sync_to_async
from django.utils.translation import gettext as _

from bot.filters import IsGameCreator
from bot.middlewares import set_random_choice_game_middlewares
from bot.models import ChatMember, Chat
from bot.models.AccessSettingsObject import AccessSettingsObject
from games.models import RandomChoiceGame, RandomChoiceGamePlayer, RandomChoiceGameResult
from .utils.keyboards import get_game_menu_keyboard
from .utils.texts import get_players, get_losers
from ..utils import mute_losers

game_router = Router()
game_router.callback_query.filter(F.data.startswith("rcg"), MagicData(F.game.is_not(None)))
set_random_choice_game_middlewares(game_router)


@game_router.callback_query(MagicData(F.game.is_finished.is_(True)))
async def finished_game_handler(callback: CallbackQuery):
    await callback.answer(_("This game is already finished"))

@game_router.callback_query(F.data.contains("join"), MagicData(F.game.is_opened_to_join.is_(True)), invert_f(IsGameCreator()))
async def join_game(callback: CallbackQuery, game: RandomChoiceGame, member: ChatMember, member_settings: AccessSettingsObject, chat: Chat):
    if not member_settings.can_join_games:
        await callback.answer(_("You cannot join games"))
        return

    if await sync_to_async(lambda: member in game.players.all())():
        await sync_to_async(game.players.remove)(member)
        await callback.answer(_("You left the game"))
    else:
        if await game.players.acount() < game.max_players_count:
            await RandomChoiceGamePlayer(game=game, chat_member=member).asave()
            await callback.answer(_("You join the game"))
        else:
            await callback.answer(_("The game already has the maximum number of players"))
            return

    await callback.message.edit_text(text=await get_players(game), reply_markup=await get_game_menu_keyboard(game))

    if game.autostart_at_max_players and await game.players.acount() == game.max_players_count:
        result: RandomChoiceGameResult = await game.start_game()

        await mute_losers(game, result, chat)

        await callback.message.edit_text(text=await get_players(game))
        await callback.message.answer(text=await get_losers(result), reply_to_message_id=callback.message.message_id)
        await callback.answer()


@game_router.callback_query(F.data.contains("start"), MagicData(F.member_settings.can_press_other_buttons.is_(True)))
@game_router.callback_query(F.data.contains("start"), IsGameCreator())
async def start_game(callback: CallbackQuery, game: RandomChoiceGame, chat: Chat):
    if await game.players.acount() < game.min_players_count:
        # Translator: can't start the game with count of players less than min_players_count
        await callback.answer(_("There are not enough players in the game"))
        return

    result: RandomChoiceGameResult = await game.start_game()

    await mute_losers(game, result, chat)

    await callback.message.edit_text(text=await get_players(game))
    await callback.message.answer(text=await get_losers(result), reply_to_message_id=callback.message.message_id)
    await callback.answer()


@game_router.callback_query(F.data.contains("delete"), MagicData(F.member_settings.can_press_other_buttons.is_(True)))
@game_router.callback_query(F.data.contains("delete"), IsGameCreator())
async def delete_game(callback: CallbackQuery, game: RandomChoiceGame, member: ChatMember):
    if await sync_to_async(lambda: game.result is not None)():
        # Translator: trying to delete a finished game
        await callback.answer(_("You can't delete a finished game"))
        return

    await game.adelete()
    # Translator: game deletion message
    await callback.answer(_("Deleted successfully"))
    await callback.message.delete()
