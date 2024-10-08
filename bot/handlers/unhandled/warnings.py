from aiogram import Router
from aiogram.types import CallbackQuery
from django.utils.translation import gettext as _

warnings_router = Router()


@warnings_router.callback_query()
async def no_access(callback: CallbackQuery):
    await callback.answer(_("Failed to process action. You may not have sufficient permissions to perform this action."))
