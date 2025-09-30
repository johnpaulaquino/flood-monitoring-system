from sqlalchemy import delete, func, update
from sqlmodel import and_, select

from app.src.database.engine_creator import create_session
from app.src.database.models import PersonalInformation, ProfileImage, Users
from app.src.database.models.announcements_model import Announcements, UpdateAnnouncements


class AnnouncementsRepository:

     @staticmethod
     async def create_announcement(announcement: Announcements, user_id):
          async with create_session() as db:
               try:
                    new_profile_img = ProfileImage(user_id=user_id)
                    db.add(new_profile_img)
                    await db.flush()
                    print('id', new_profile_img.id)
                    announcement.image_url_id = new_profile_img.id
                    db.add(announcement)
                    await db.commit()
               except Exception as e:
                    await db.rollback()
                    raise e

     @staticmethod
     async def get_specific_announcement(user_id, announcement_id):
          async with create_session() as db:
               try:
                    stmt_sub = (
                            select(
                                    Announcements.id,
                                    Announcements.title,
                                    Announcements.content,
                                    Announcements.created_at,
                                    Announcements.image_url_id,
                            )
                            .where(and_(Announcements.user_id == user_id, Announcements.id == announcement_id))
                            .order_by(Announcements.created_at)
                            .subquery()
                    )
                    # # Main Query
                    stmt = (
                            select(
                                    stmt_sub,
                                    func.array_agg(ProfileImage.img_url).label('img_url'),
                                    func.array_agg(ProfileImage.public_key).label('public_key'),
                                    )
                            .outerjoin(stmt_sub, ProfileImage.id == stmt_sub.c.image_url_id)
                            .where(and_(ProfileImage.user_id == user_id, Announcements.id == announcement_id))
                            .group_by(
                                    stmt_sub))
                    result = await db.execute(stmt)
                    data = result.mappings().fetchone()
                    return data
               except Exception as e:
                    raise e

     @staticmethod
     async def get_ten_announcements(user_id: str):
          async with create_session() as db:
               try:

                    stmt_sub = (
                            select(
                                    PersonalInformation.firstname,
                                    PersonalInformation.middle_name,
                                    PersonalInformation.last_name,
                                    Announcements.title,
                                    Announcements.content,
                                    Announcements.created_at,
                                    Announcements.image_url_id,
                            )
                            .select_from(Users)
                            .outerjoin(Announcements, Users.id == Announcements.user_id)
                            .outerjoin(PersonalInformation, Users.id == PersonalInformation.user_id)
                            .where(Announcements.user_id == user_id)
                            .order_by(Announcements.created_at)
                            .limit(10)
                            .subquery()
                    )

                    stmt = (
                            select(
                                    stmt_sub,
                                    func.array_agg(ProfileImage.img_url).label('image'))
                            .outerjoin(ProfileImage, ProfileImage.id == stmt_sub.c.image_url_id)
                            .where(ProfileImage.user_id == user_id)
                            .group_by(
                                    stmt_sub, )
                    )
                    result = await db.execute(stmt)
                    data = result.mappings().fetchmany()
                    return data
               except Exception as e:
                    raise e

     @staticmethod
     async def get_paginated_announcements(user_id: str, offset: int, limit: int = 10):
          async with create_session() as db:
               try:
                    # Subquery
                    stmt_sub = (
                            select(
                                    PersonalInformation.firstname,
                                    PersonalInformation.middle_name,
                                    PersonalInformation.last_name,
                                    Announcements.id,
                                    Announcements.title,
                                    Announcements.content,
                                    Announcements.created_at,
                                    Announcements.image_url_id,
                            )
                            .select_from(Users)
                            .outerjoin(Announcements, Users.id == Announcements.user_id)
                            .outerjoin(PersonalInformation, Users.id == PersonalInformation.user_id)
                            .where(Announcements.user_id == user_id)
                            .order_by(Announcements.created_at)
                            .limit(limit)
                            .offset(offset)
                            .subquery())
                    # Main Query
                    stmt = (
                            select(
                                    stmt_sub,
                                    func.array_agg(ProfileImage.img_url).label('image'))
                            .outerjoin(ProfileImage, ProfileImage.id == stmt_sub.c.image_url_id)
                            .where(ProfileImage.user_id == user_id)
                            .group_by(
                                    stmt_sub, )
                    )
                    result = await db.execute(stmt)
                    data = result.mappings().fetchall()
                    return data
               except Exception as e:
                    raise e

     @staticmethod
     async def update_announcements(user_id: str, announce_id: str, announcement: UpdateAnnouncements):
          async with create_session() as db:
               try:

                    stmt = update(Announcements).values(
                            announcement.model_dump(exclude_unset=True),
                    ).where(and_(
                            Announcements.id == announce_id,
                            Announcements.user_id == user_id))
                    await db.execute(stmt)
                    await db.commit()
               except Exception as e:
                    await db.rollback()
                    raise e

     @staticmethod
     async def delete_announcement(user_id: str, announce_id: str):
          async with create_session() as db:
               try:
                    stmt = delete(Announcements).where(
                            and_(Announcements.id == announce_id, Announcements.user_id == user_id))
                    await db.execute(stmt)
                    await db.commit()
               except Exception as e:
                    await db.rollback()
                    raise e
