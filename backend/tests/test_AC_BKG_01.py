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
    # ยังไม่ตรวจหมายเลขคิว เพราะรอ Q-02; หน้าจออยู่ใน TC-BKG-01-2


def test_TC_BKG_01_3_full_slot(client, make_slot, db):
    from app.db.models import Booking
    # Given ยืนยันตัวตนแล้ว ช่วง 09.00 น. เหลือ 0 ที่
    # วันเดียวกันและวันถัดไปมีช่วงว่างอย่างน้อย 3 ช่วง
    slot = make_slot(start="09:00", remaining=0)
    alternatives = [
        make_slot(start="09:30", remaining=1),
        make_slot(start="08:00", remaining=1, days_from_today=2),
        make_slot(start="09:00", remaining=1, days_from_today=2),
    ]
    make_slot(start="10:00", remaining=1, days_from_today=2)
    make_slot(start="09:00", remaining=1, days_from_today=3)
    # When ยืนยันการจองช่วง 09.00 น.
    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)
    # Then ตอบ 409 และไม่สร้างรายการจอง
    assert res.status_code == 409
    db.expire_all()
    assert db.query(Booking).count() == 0
    # Then มี 3 ช่วงว่างใกล้ที่สุดในวันเดียวกันและวันถัดไป
    # ใช้ slot_id ของข้อมูลช่วงเวลา โดยไม่กำหนดชื่อ envelope เอง
    def slot_ids(value):
        if isinstance(value, dict):
            result = [value["slot_id"]] if "slot_id" in value else []
            return result + [item for key, child in value.items()
                             if key != "slot_id" for item in slot_ids(child)]
        if isinstance(value, list):
            return [item for child in value for item in slot_ids(child)]
        return []
    assert sorted(slot_ids(res.json())) == sorted(s.id for s in alternatives)


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
