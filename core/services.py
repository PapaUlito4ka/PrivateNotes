from typing import Type, List, Any

from django.db.models import Prefetch
from django.http import QueryDict
from django.core.paginator import Paginator

from core.models import Note, User


class UserService:

    @staticmethod
    def create(raw_user: Type[QueryDict]) -> User:
        if isinstance(raw_user, QueryDict):
            raw_user = raw_user.dict()
        return User.objects.create_user(
            username=raw_user['email'],
            password=raw_user['password'],
        )

    @staticmethod
    def authenticate(username: str, password: str) -> Any:
        user = User.objects.get(username=username)
        if user.password != password:
            return None
        return user


class NoteService:

    NOTE_PER_PAGE = 20

    @staticmethod
    def create(raw_note: Type[QueryDict], user_id: int) -> User:
        if isinstance(raw_note, QueryDict):
            raw_note = raw_note.dict()
        return Note.objects.create(
            text=raw_note['text'],
            user_id=user_id
        )

    @staticmethod
    def list(user_id: int, page_num: int = 1):
        p = Prefetch('user')
        p = Paginator(
            Note.objects.prefetch_related(p).filter(user_id=user_id).values_list(),
            NoteService.NOTE_PER_PAGE
        )
        cur_page = p.page(page_num)
        return {
            'count': p.count,
            'prev': cur_page.previous_page_number() if cur_page.has_previous() else None,
            'next': cur_page.next_page_number() if cur_page.has_next() else None,
            'cur': cur_page.number,
            'data': [Note.objects.get(pk=note[0]) for note in cur_page.object_list]
        }
