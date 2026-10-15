# RTM: จองคิวตรวจสุขภาพ (Booking)
อ้างอิง: spec.md SPEC-BKG-001 Draft v2 | plan.md v1 | tasks.md | test-cases.md
สร้างด้วย /verify เมื่อ 2569-10-14 | commit ที่ตรวจ: b0cd190

ตรวจเฉพาะรายงาน ไม่แก้โค้ด test spec plan หรือ tasks

## ผลทดสอบ

- หลังบ้าน: `pytest -v` ผ่าน 8 ตัว ไม่ผ่าน 0 ตัว มี Starlette/httpx deprecation warning 1 รายการ
- หน้าจอ: `npm test -- --reporter=verbose` ผ่าน 1 ตัว ข้าม 1 ตัว และล้ม 1 suite (`frontend/tests/researchFilter.test.mjs`: No test suite found)
- ข้อความผ่าน 2 ตัวจาก node:test ในไฟล์ researchFilter ไม่ใช่ผลผ่านของ Vitest; คำสั่ง npm test จบด้วย exit code 1
- ผล test ผ่านไม่ได้ยืนยันทุก requirement โดยเฉพาะงานที่ยังไม่ทำและ Q-02

| Test | ผล | สิ่งที่ตรวจจริง |
|---|---|---|
| test_AC_BKG_01 | ผ่าน | HTTP 201 เท่านั้น |
| test_TC_BKG_01_1_book_last_seat | ผ่าน | มีการจอง 1 รายการ ID/slot/HN ถูกต้อง และ remaining เป็น 0 |
| test_TC_BKG_01_2_no_seat_left | ผ่าน | หลังคนอื่นจองที่สุดท้าย ตอบ 409 ไม่เพิ่มรายการ และ remaining ยังเป็น 0 |
| test_TC_BKG_01_3_not_verified | ผ่าน | ไม่มี Authorization ตอบ 401 ไม่มีการจอง และ remaining ยังเป็น 1 |
| test_TC_BKG_01_4_unverified_user | ผ่าน | ไม่มี Authorization ตอบ 4xx และไม่เรียกบริการจอง |
| test_AC_BKG_05 | ผ่าน | 200 คำขอเรียงทีละคำขอ HTTP 200 และ p95 ไม่เกิน 2 วินาที |
| test_T01_tables_created | ผ่าน | สร้างตาราง slots/bookings/audit_logs บน SQLite |
| test_T01_no_national_id | ผ่าน | ตาราง bookings ไม่มี national_id และมี hn |
| โครงหน้าจอเปิดได้ | ผ่าน | แสดงหัวเรื่องของ App |
| TC-BKG-01-1 แสดงหมายเลขคิว (ไฟล์ TC-BKG-01-2.test.jsx) | ข้าม | รอ Q-02 ไม่มี assert |
| researchFilter.test.mjs | suite ล้ม | ใช้ node:test ไม่ใช่ suite ของ Vitest |

## 1. ตามรอยไปข้างหน้า (requirement ไป โค้ด ไป test)

หนึ่งแถวต่อ FR/NFR/CON/DOM/IF รวม 15 แถว: ครบ 0, ยังไม่ถึง 8, รอ 0, ช่องโหว่ 7
สถานะรอ Q-02 ของส่วนเลขคิวระบุในรายละเอียด FR-BKG-04 แต่สถานะรวมเป็นช่องโหว่เพราะมีโค้ดเดาคำตอบแล้ว

| ID | AC | task | โค้ด (ไฟล์: ฟังก์ชัน) | test (ผล) | สถานะ |
|---|---|---|---|---|---|
| FR-BKG-01 | AC-BKG-05 ตรวจความเร็ว ไม่ตรวจเนื้อหา | T-02 เสร็จ; T-10/T-12 ยังไม่ทำ | backend/app/slots/router.py: get_slots; slots/service.py: list_available_slots กรองวัน/แพ็กเกจ/remaining แต่ใช้ 14 วัน | test_AC_BKG_05 ผ่าน แต่ไม่ตรวจวันหรือข้อมูลที่นั่ง; F-06/F-07 | ช่องโหว่ |
| FR-BKG-02 | AC-BKG-02 | T-04 พร้อมทำ | booking/service.py: create_booking ยังไม่ตรวจคิวเดิม; ไม่มีหน้าจอแสดงเลขเดิม | ยังไม่มี test; task ยังไม่ทำ ไม่จัดเป็น AC ไม่มี test | ยังไม่ถึง |
| FR-BKG-03 | AC-BKG-03 | T-05/T-11/T-12 พร้อมทำ | booking/router.py ตอบ 409 ข้อความเต็ม แต่ไม่มี 3 ช่วง; ยังไม่มีหน้าจอ | TC-BKG-01-2 ผ่านเฉพาะ 409/ไม่มีการจอง/remaining ไม่ใช่ AC-BKG-03 ทั้งหมด | ยังไม่ถึง |
| FR-BKG-04 | AC-BKG-01 | T-03 เสร็จ; T-06 รอ Q-02; T-07 ยังไม่ทำ | booking/service.py: create_booking บันทึกและตัดที่นั่ง; next_queue_no เดารูปแบบ; ยังไม่มีคำขอแจ้งเตือน | test_AC_BKG_01 และ TC-BKG-01-1/2 ผ่าน; display skipped รอ Q-02; F-03/F-05 | ช่องโหว่ |
| FR-BKG-05 | AC-BKG-04 | T-07 พร้อมทำ; ส่วนแสดงเลขคิวรอ Q-02 | ไม่มี notify/queue.py หรือ BookingResult; GET /bookings/{id} ตาม plan ยังไม่มี | ไม่มี test งาน T-07 ยังไม่ทำ | ยังไม่ถึง |
| FR-BKG-06 | ไม่มี AC | T-02 เสร็จ; T-10/T-12 พร้อมทำ | slots/service.py กรอง package_code; api/client.js รับ packageCode; ยังไม่มีหน้าจอเปลี่ยนแพ็กเกจ | ไม่มี test ตรวจการเปลี่ยนแพ็กเกจ; F-08 | ช่องโหว่ |
| NFR-PERF-01 | AC-BKG-05 | T-02 เสร็จ | GET /slots | test_AC_BKG_05 ผ่าน แต่ยิงเรียงลำดับ ไม่ใช่ผู้ใช้พร้อมกัน 200 คน; F-09 | ช่องโหว่ |
| NFR-SEC-01 | ไม่มี AC | ไม่มี task รองรับโดยตรงใน tasks.md | ไม่พบหลักฐานตั้งค่า TLS 1.2+ ในขอบเขตไฟล์ที่ตรวจ; อาจเป็นงาน deployment ที่ยังไม่ระบุ | ไม่มี test TLS | ยังไม่ถึง |
| NFR-REL-02 | AC-BKG-04 | T-07 พร้อมทำ | ยังไม่มีคิวส่งซ้ำหรือเวลา 5 นาที | ไม่มี test งานยังไม่ทำ | ยังไม่ถึง |
| NFR-USE-01 | ไม่มี AC | ไม่มี task ทดลองผู้ใช้โดยตรง | ยังมีเพียงโครง App; หน้าจอ T-10 เป็นต้นไปยังไม่ทำ | ไม่มีผลอาสาสมัคร 10 คน/8 คนทำสำเร็จภายใน 3 นาที | ยังไม่ถึง |
| CON-TECH-01 | ไม่มี AC | T-01 เสร็จ | config.py/session.py รองรับ DATABASE_URL; ค่าเริ่มต้น SQLite สำหรับทดลองตาม plan | schema tests ผ่านบน SQLite เท่านั้น ไม่ยืนยัน PostgreSQL; F-11 | ช่องโหว่ |
| DOM-PDPA-01 | AC-BKG-06 | T-01 เสร็จเฉพาะตาราง; T-08 พร้อมทำ | models.py: AuditLog มี actor/action/hn/time แต่ไม่มี middleware บันทึกการเข้าถึงหรือ retention | schema test ไม่ใช่ audit behavior; T-08 ยังไม่ทำ | ยังไม่ถึง |
| IF-IDP-01 | ไม่มี AC ตรง; TC-BKG-01-3/4 จาก AC-BKG-01 ตรวจ precondition | T-03 เสร็จ | auth/idp.py: get_verified_hn ตรวจเพียง prefix ของข้อความ token | TC-BKG-01-3/4 ผ่านเฉพาะไม่มี token ไม่ยืนยันว่าได้รับผลจาก IdP จริง; F-02 | ช่องโหว่ |
| IF-HIS-01 | ไม่มี AC | T-01 เสร็จ; T-09 พร้อมทำ | bookings เก็บ HN ไม่มี national_id; BookingRequest รับ national_id และ logger เขียนลง log; HIS ยังไม่ทำ | test_T01_no_national_id ผ่านเฉพาะ schema; F-01 | ช่องโหว่ |
| IF-NOT-01 | ไม่มี AC ตรง; AC-BKG-04 ตรวจกรณีแจ้งเตือนล้ม | T-07 พร้อมทำ | ยังไม่มีการส่งคำขอ/คิว SMS/LINE แบบ async | ไม่มี test งานยังไม่ทำ | ยังไม่ถึง |

## 2. ตามรอยย้อนกลับ (โค้ด ไป requirement)

| โค้ด (ไฟล์: ฟังก์ชัน หรือ endpoint) | อ้าง ID | ตรงกับข้อความใน spec ไหม | หมายเหตุ |
|---|---|---|---|
| config.py: DATABASE_URL; db/session.py: engine/get_db | CON-TECH-01 | รองรับ PostgreSQL ผ่าน env | SQLite ทดลองอนุญาตใน plan; ไม่ถือเป็นการละเมิดเพราะค่า default เพียงอย่างเดียว แต่ไม่มีผลตรวจ PostgreSQL |
| db/models.py: Slot | FR-BKG-01/06, ASM-01 | มีวัน/เวลา/แพ็กเกจ/โควตา/remaining | อ่านโควตา ไม่เพิ่ม API จัดการโควตาที่อยู่นอกขอบเขต |
| db/models.py: Booking | FR-BKG-04, IF-HIS-01 | บันทึก HN/slot/date/queue/status/time | ตารางไม่มีเลขบัตร; queue nullable ตาม plan |
| db/models.py: AuditLog | DOM-PDPA-01 | มีโครงฟิลด์ | การบันทึกจริงและเก็บอย่างน้อย 1 ปีเป็น T-08 ที่ยังไม่ทำ |
| db/migrations/001_init.py: upgrade | CON-TECH-01, DOM-PDPA-01, IF-HIS-01 | สร้างตาราง | schema tests ไม่ใช่การตรวจ behavior ของทุก constraint |
| main.py: lifespan และ router registration | T-01/02/03 | โครงสร้างระบบ | สร้างตารางเมื่อเริ่ม ไม่มี middleware audit ในรอบนี้ |
| auth/idp.py: get_verified_hn/PREFIX | IF-IDP-01 | เป็น mock เท่านั้น | อ่าน HN จาก token ที่ caller เขียนเอง; F-02 |
| GET /slots: get_slots | FR-BKG-01/06 | คืน slot_id/date/time/remaining และกรองแพ็กเกจ | ไม่มีข้อมูลผู้รับบริการใน response นี้ จึงไม่สรุปละเมิด IF-IDP จากไม่มี auth ใน endpoint นี้เพียงอย่างเดียว |
| slots/service.py: list_available_slots/DAYS_AHEAD | FR-BKG-01/06 | ระยะวันไม่ตรง | 14 แทน 30 วัน; F-06 |
| POST /bookings: create_booking | FR-BKG-04, IF-IDP-01 | บันทึกและตัดที่นั่งได้ | response booking_id/slot_id/queue_no; 409 มีแต่ข้อความ; T-04/05/07 ยังไม่ทำ |
| booking/router.py: BookingRequest และ logger.info | IF-HIS-01 | national_id ไม่อยู่ใน input ของ POST ตาม plan | รับเลขบัตรโดยไม่ค้น HIS และเขียนลง log; F-01 |
| booking/service.py: create_booking | FR-BKG-04 | remaining <= 0 ปฏิเสธ; เมื่อสำเร็จ remaining -= 1 | มี test ตรวจบันทึก/ตัดที่นั่ง/ขอบ 0; ไม่มีการทำ notification ซึ่งรอ T-07 |
| booking/service.py: next_queue_no | FR-BKG-04 | กำหนดรูปแบบ A001 และนับรายวันก่อน Q-02 ตอบ | F-03 |
| DELETE /bookings/{booking_id}: cancel_booking; service.cancel_booking | คอมเมนต์ FR-BKG-04 | ไม่ตรง; อยู่ใน Out of scope UC-02 | คืนที่นั่ง เปลี่ยนสถานะ CANCELLED; F-04/F-05 |
| frontend/src/api/client.js: getSlots/createBooking | FR-BKG-01/04/06 ตาม plan | เป็น client scaffold | ไม่มีการแนบผล IdP; การต่อหน้าจอจริง T-12 ยังไม่ทำ |
| frontend/src/App.jsx/main.jsx/index.css | โครงเริ่มต้น | ยังไม่ใช่หน้า UC-01 | setup test ตรวจหัวเรื่องเท่านั้น ไม่ถือว่าตอบ FR แล้ว |
| frontend/src/researchFilter.ts: filterResearches | ไม่มี ID/task ของ Booking | ไม่ตรง | ค้นงานวิจัย/SDGs และ import research ที่ไม่มีไฟล์; F-10 |

## 3. ข้อค้นพบ

ชนิด: AC ไม่มี test / test อ่อน / โค้ดไม่มี FR / FR ไม่มี AC / เดา Q-xx / ละเมิด Constraint / ตัวเลขไม่ตรง spec / อ้าง ID ผิดเรื่อง
ช่องทีมตัดสินเว้นให้ทีมกรอก ไม่ถือเป็นคำตัดสินของ AI

| F-ID | ชนิด | อยู่ที่ | ขัดกับ | รายละเอียด | ทีมตัดสิน |
|---|---|---|---|---|---|
| F-01 | ละเมิด Constraint | backend/app/booking/router.py:19,25 | IF-HIS-01; plan ข้อ 4 | POST รับ national_id ทั้งที่ input การจองระบุ slot_id เท่านั้น แล้ว logger.info เขียนเลขบัตรลง log โดยไม่ได้ใช้ค้น HIS; การไม่มีคอลัมน์ใน bookings ไม่ครอบคลุมการเก็บใน log; ผล schema test จึงไม่ยืนยัน constraint ทั้งหมด | |
| F-02 | ละเมิด Constraint | backend/app/auth/idp.py:4–15 | IF-IDP-01 | token เป็นเพียงข้อความ Bearer verified:<HN> ที่ผู้เรียกสร้างเอง ไม่มีการตรวจผล IdP และรับ HN ว่างได้; เป็น mock ที่ต้องแยกจากหลักฐานยืนยันตัวตนจริง; test ตรวจไม่มี token เท่านั้นไม่ตรวจ token ปลอม | |
| F-03 | เดา Q-02 | backend/app/booking/service.py:13–18,34 | Q-02; plan ข้อ 8; T-06 | next_queue_no ใช้ A001 และนับใหม่รายวัน ทั้งที่ Q-02 ยังไม่ตอบ; A001 เป็นเพียงตัวอย่างในคำถาม ไม่ใช่คำตอบของทีม | |
| F-04 | โค้ดไม่มี FR | backend/app/booking/router.py:35–41; service.py:42–50 | Out of scope UC-02; plan ข้อ 4 | มี DELETE /bookings/{booking_id} ยกเลิกการจอง/คืนที่นั่ง เปลี่ยน CANCELLED; อยู่ใน Out of scope และไม่มี task รองรับ ไม่ใช่รายละเอียดเทคนิคที่ทีมเลือกเอง | |
| F-05 | อ้าง ID ผิดเรื่อง | docstring cancel_booking ใน booking/router.py และ service.py | FR-BKG-04 | คอมเมนต์ยกเลิกอ้าง FR-BKG-04 แต่ FR นี้กำหนดยืนยันสำเร็จ/บันทึก/ตัดที่นั่ง/ออกคิว/ส่งคำขอข้อความ ไม่ได้อนุญาตยกเลิก | |
| F-06 | ตัวเลขไม่ตรง spec | backend/app/slots/service.py:10 | FR-BKG-01 | DAYS_AHEAD = 14 แต่ spec กำหนด 30 วัน; test ปัจจุบันไม่สร้างวัน 15–30 จึงไม่จับปัญหานี้ | |
| F-07 | FR ไม่มี AC | spec.md: FR-BKG-01 และ Traceability | FR-BKG-01 | AC-BKG-05 ที่ผูกกับ FR นี้ตรวจแต่ความเร็ว ไม่ตรวจแสดงวัน/ช่วงว่าง/remaining และขอบเขต 30 วัน จึงไม่มี AC ที่ตรวจผลของ FR นี้โดยตรง | |
| F-08 | FR ไม่มี AC | spec.md: FR-BKG-06; plan ข้อ 6 | FR-BKG-06 | ไม่มี AC สำหรับเปลี่ยนแพ็กเกจแล้วคำนวณช่วงว่างใหม่ แม้ T-02 มี code กรองแพ็กเกจและ T-10 ยังไม่ทำ; เป็นช่องว่างของ spec | |
| F-09 | test อ่อน | backend/tests/test_AC_BKG_05.py:10–20 | AC-BKG-05, NFR-PERF-01 | ส่ง 200 คำขอเรียงลำดับ ไม่พร้อมกัน จึงตรวจ p95 ภายใต้โหลดตาม Given ไม่ได้; plan อนุญาตแบบย่อส่วนแต่ไม่ควรสรุป requirement จริงครบจากผลนี้ | |
| F-10 | โค้ดไม่มี FR | frontend/src/researchFilter.ts; frontend/tests/researchFilter.test.mjs | SPEC-BKG-001; tasks.md | ฟังก์ชันค้นงานวิจัย/SDGs ไม่มี requirement หรือ task ของ Booking และ import ./research ซึ่งไม่มีใน src; test เก่าทำให้ npm test ล้มเพราะใช้ node:test; เป็นไฟล์จริงใน repo ไม่ใช่หน้าจอ Booking ที่ยังไม่ได้ทำ | |
| F-11 | test อ่อน | backend/tests/test_T01_schema.py; tests/conftest.py | CON-TECH-01 | test ทั้งหมดใช้ SQLite ไม่มี test PostgreSQL หรือหลักฐาน DATABASE_URL ของระบบจริง; ยืนยันได้เพียง schema/behavior ในฐานข้อมูลจำลอง ไม่ยืนยันข้อบังคับ PostgreSQL; ไม่สรุปว่าระบบจริงใช้ SQLite เพราะไม่ได้ตรวจ deployment | |

### ตรวจ Then และรายการที่ไม่จัดเป็นข้อค้นพบ

- AC-BKG-01: บันทึกและ remaining เป็น 0 มี assert จริงใน TC-BKG-01-1; test_AC_BKG_01 เดิมตรวจเพียง 201 แต่มี test ใหม่เสริมแล้ว จึงไม่รายงานว่าไม่มีใครตรวจการตัดที่นั่ง
- หากลบ remaining -= 1 ออก TC-BKG-01-1 จะไม่ผ่าน และ TC-BKG-01-2 จะไม่ผ่านขั้นเตรียมที่นั่งเต็ม จึงไม่ใช่ช่องโหว่แบบ test อ่อนเดิมในส่วนนี้
- การแสดงเลขคิวรอ Q-02 มี skipped placeholder ไม่มี assert ตามข้อกำหนด; ไม่ถือเป็น AC ไม่มี test ที่ต้องทำเสร็จในตอนนี้
- แถวใช้ได้ TC-BKG-01-1 ถึง TC-BKG-01-4 มี test ตามส่วนที่ตัดสินแล้วครบ; TC-BKG-01-3/4 Given คล้ายกันแต่ตรวจผล/การไม่เรียก service ต่างกัน ไม่เพิ่มข้อค้นพบจากความซ้ำเพียงอย่างเดียว
- AC-BKG-02/03/04/06 ผูกกับ task ที่ยังไม่ทำ ไม่รายงาน AC ไม่มี test; TC-BKG-01-2 ไม่ทดแทนการตรวจ 3 ช่วงว่างของ AC-BKG-03
- FR-BKG-04 ส่วนส่งคำขอข้อความเป็น T-07 ที่ยังไม่ทำ; ไม่มี test ไม่ใช่ช่องโหว่ของ task เสร็จในขอบเขต T-03
- TLS, การเก็บ audit 1 ปี และ usability ยังไม่มีหลักฐานตรวจจริง รายงานความไม่ครบไว้ในตาราง ไม่เดาว่ามีการตั้งค่าภายนอกหรือมีผลผู้ใช้แล้ว

## 4. แก้แล้ว

ยังไม่มี rtm.md เดิม จึงไม่มี F-ID เก่าที่จะย้ายหรือช่องทีมตัดสินเดิมให้รักษา

| F-ID | แก้อย่างไร | รู้ได้อย่างไร |
|---|---|---|

หลักฐานเพิ่มเติม: ปัญหา remaining < 0 เดิมแก้เป็น <= 0 ใน commit 8efbea5 แล้ว; TC-BKG-01-2 ปัจจุบันผ่าน 409/ไม่มีรายการใหม่/remaining 0 แต่ไม่สร้าง F-ID ย้อนหลังให้เรื่องที่แก้ก่อนรายงานนี้

ข้อค้นพบทั้งหมด AI เป็นคนตรวจ และอาจหาไม่ครบ ทีมต้องเปิดโค้ดและ spec ยืนยันทีละข้อ แล้วเขียนช่อง 'ทีมตัดสิน' เอง
