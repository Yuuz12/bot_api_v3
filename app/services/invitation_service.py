from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models.invitation import InvitationCode, InvitationQQ, InvitationNumber
from app.exceptions import NotFoundError, BadRequestError, ConflictError
from datetime import datetime


class InvitationService:
    @staticmethod
    async def obtain_invitation_code(db: AsyncSession, qq: str) -> dict:
        result = await db.execute(select(InvitationQQ).where(InvitationQQ.qq == qq))
        existing = result.scalar_one_or_none()
        if existing:
            raise ConflictError("该QQ号已获取过邀请码")

        result = await db.execute(select(InvitationNumber).limit(1))
        number_entry = result.scalar_one_or_none()
        if not number_entry:
            number_entry = InvitationNumber(number=0)
            db.add(number_entry)
            await db.flush()

        number_entry.number += 1
        current_number = number_entry.number
        await db.flush()

        result = await db.execute(select(InvitationCode).where(InvitationCode.id == current_number))
        code_entry = result.scalar_one_or_none()
        code = code_entry.code if code_entry else f"INV-{current_number:06d}"

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        invitation_qq = InvitationQQ(qq=qq, number=current_number, codes=code, time=now)
        db.add(invitation_qq)
        await db.flush()
        return {"qq": qq, "code": code, "number": current_number}

    @staticmethod
    async def query_invitation_code(db: AsyncSession, qq: str) -> dict:
        result = await db.execute(select(InvitationQQ).where(InvitationQQ.qq == qq))
        entry = result.scalar_one_or_none()
        if not entry:
            raise NotFoundError("未找到该QQ号的邀请码记录")
        return {"qq": entry.qq, "number": entry.number, "codes": entry.codes, "time": entry.time}
