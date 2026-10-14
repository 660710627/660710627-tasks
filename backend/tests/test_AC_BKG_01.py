# test ของ T-03: จองคิวสำเร็จ
# AC-BKG-01 (FR-BKG-04)
from tests.conftest import AUTH


def test_AC_BKG_01(client, make_slot):
    """AC-BKG-01: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง จองแล้วต้องสำเร็จ"""
    slot = make_slot(start="09:00", remaining=1)

    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    assert res.status_code == 201


def test_TC_BKG_01_1_book_last_seat(client, make_slot, db):
    from app.db.models import Booking
    # Given ยืนยันตัวตนแล้ว ช่วง 09.00 น. มีที่นั่งว่าง 1 ที่
    slot = make_slot(start="09:00", remaining=1)
    # When ยืนยันการจองผ่าน POST /bookings
    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)
    # Then มีการจองถูกบันทึกสำเร็จ และที่นั่งว่างเป็น 0
    assert res.status_code == 201
    db.expire_all()
    bookings = db.query(Booking).all()
    assert len(bookings) == 1
    assert bookings[0].id == res.json()["booking_id"]
    assert bookings[0].slot_id == slot.id
    assert bookings[0].hn == "0001234"
    db.refresh(slot)
    assert slot.remaining == 0
    # ยังไม่ตรวจการแสดงหมายเลขคิวของ TC-BKG-01-1 เพราะรอ Q-02


def test_TC_BKG_01_3_not_verified(client, make_slot, db):
    from app.db.models import Booking
    # Given ยังไม่ได้ยืนยันตัวตน และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่
    slot = make_slot(start="09:00", remaining=1)
    # When ยืนยันการจองช่วง 09.00 น.
    res = client.post("/bookings", json={"slot_id": slot.id})
    # Then (1) ปฏิเสธ ตอบ 401
    assert res.status_code == 401
    # Then (2) ไม่มีการจอง
    db.expire_all()
    assert db.query(Booking).count() == 0
    # Then (3) ที่นั่งว่างยังเป็น 1
    db.refresh(slot)
    assert slot.remaining == 1


def test_TC_BKG_01_4_unverified_user(client, make_slot):
    from unittest.mock import patch
    # Given ยังไม่ยืนยันตัวตน ช่วง 09.00 น. ว่าง 1 ที่
    slot = make_slot(start="09:00", remaining=1)
    # When ส่งคำขอยืนยันการจองโดยไม่มีผลยืนยันตัวตน
    with patch("app.booking.router.service.create_booking") as create_booking:
        res = client.post("/bookings", json={"slot_id": slot.id})
    # Then ไม่อนุญาตเข้าถึงบริการข้อมูลการจองตาม IF-IDP-01
    assert 400 <= res.status_code < 500
    create_booking.assert_not_called()
    # ไม่ assert status ที่แน่นอน ข้อความ และผลต่อข้อมูล/ที่นั่งที่ spec ไม่บอก


def test_TC_BKG_01_2_no_seat_left(client, make_slot, db):
    from app.db.models import Booking
    # Given ยืนยันตัวตนแล้ว ช่วง 09.00 น. เหลือ 0 ที่ มีคนจองที่สุดท้ายไปแล้ว
    slot = make_slot(start="09:00", remaining=1)
    previous = client.post(
        "/bookings", json={"slot_id": slot.id},
        headers={"Authorization": "Bearer verified:0005678"},
    )
    assert previous.status_code == 201
    db.refresh(slot)
    assert slot.remaining == 0
    original_ids = {booking.id for booking in db.query(Booking).all()}
    # When ผู้รับบริการยืนยันการจองช่วง 09.00 น.
    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)
    # Then (1) ปฏิเสธ ตอบ 409
    assert res.status_code == 409
    # Then (2) ไม่มีการจองใหม่ โดยคงการจองเดิมไว้
    db.expire_all()
    assert {booking.id for booking in db.query(Booking).all()} == original_ids
    # Then (3) ที่นั่งว่างยังเป็น 0 ไม่ติดลบ
    db.refresh(slot)
    assert slot.remaining == 0
