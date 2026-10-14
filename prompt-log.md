# Prompt log

บันทึกทุกครั้งที่ใช้ AI กับ repo นี้ เขียนต่อท้ายเรื่อย ๆ ไม่ลบของเก่า

---

## 2569-09-23 13.40 คำสั่ง: /tasks specs/001-booking/spec.md

- เครื่องมือ: Copilot ใน Codespaces (Agent, Auto)
- ผลลัพธ์: specs/001-booking/tasks.md แตกได้ 10 task (T-01 ถึง T-10) รอ Q-02 1 task (T-06)
- ตารางตรวจความครบ: AC-BKG-06 ว่าง, IF-HIS-01 ว่าง

### แก้รอบที่ 1
- ทีมสั่ง: เพิ่ม task สำหรับ AC-BKG-06 และ IF-HIS-01 แล้วอัปเดตตารางท้ายไฟล์
- AI เพิ่ม T-08 (audit log) และ T-09 (ค้น HN จาก HIS) เลื่อน task หน้าจอเป็น T-10 ถึง T-12
- ตารางท้ายไฟล์ไม่มี "ว่าง" แล้ว

---

## 2569-09-23 14.20 คำสั่ง: /implement T-01 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/config.py, backend/app/db/models.py, backend/app/db/session.py, backend/app/db/migrations/001_init.py, backend/tests/test_T01_schema.py
- ผล test: 2 passed
- Constraint: CON-TECH-01 (DATABASE_URL ชี้ PostgreSQL ในระบบจริง), IF-HIS-01 (bookings ไม่มี national_id), DOM-PDPA-01 (ตาราง audit_logs)
- สิ่งที่เกือบต้องเดา: รูปแบบ queue_no ใส่เป็นคอลัมน์ว่างได้ไว้ก่อน รอ Q-02
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-09-27 19.05 คำสั่ง: /implement T-02 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/slots/router.py, backend/app/slots/service.py, backend/app/main.py, backend/tests/conftest.py, backend/tests/test_AC_BKG_05.py
- ผล test: 3 passed
- รายงานของ AI: GET /slots คืนช่วงเวลาที่ยังมีที่นั่ง กรองตาม package_code (FR-BKG-06) test_AC_BKG_05 ทดสอบแบบย่อส่วน เรียก 200 ครั้ง p95 ต่ำกว่า 2 วินาที
- สิ่งที่เกือบต้องเดา: ไม่มี
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-09-28 20.30 คำสั่ง: /implement T-03 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/booking/router.py, backend/app/booking/service.py, backend/app/auth/idp.py และแก้ backend/app/main.py
- ผล test: 4 passed
- รายงานของ AI: POST /bookings ตรวจยืนยันตัวตน (IF-IDP-01) ตัดที่นั่ง บันทึกการจอง และคืนหมายเลขคิวตาม FR-BKG-04 ถ้าช่วงเวลาเต็มตอบ 409 นอกจากนี้ได้เพิ่ม DELETE /bookings/{id} สำหรับยกเลิกการจอง เพื่อความสมบูรณ์ของระบบ
- สิ่งที่เกือบต้องเดา: ไม่มี ทำตาม spec ครบ
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-10-07 คำสั่ง: /testcases AC-BKG-01 specs/001-booking/

- โหมด: ร่าง (ยังไม่มีแถวของ AC-BKG-01 ใน test-cases.md)
- อ่าน: AGENTS.md, .claude/commands/testcases.md และ spec.md, plan.md, tasks.md, test-cases.md ของ specs/001-booking/
- แผน: เพิ่มกรณีทางปกติหลังบ้านและหน้าจอ ขอบที่นั่งเหลือ 0 และทางผิดที่ยังไม่ยืนยันตัวตน แล้วหยุดให้ทีมตรวจตาราง
- TC ID ที่เสนอ: TC-BKG-01-1, TC-BKG-01-2, TC-BKG-01-3, TC-BKG-01-4 (สถานะร่างทุกแถว)
- ครอบคลุม Then ของ AC-BKG-01: บันทึกสำเร็จ, ที่นั่งว่างเป็น 0 และแสดงหมายเลขคิว (รอ Q-02)
- สถานะ task: T-03 เสร็จ; T-06 รอ Q-02
- คำถามที่ยังต้องให้ทีมตอบ: Q-02 รูปแบบและวิธีออกหมายเลขคิว; เมื่อยังไม่ยืนยันตัวตน API ต้องตอบ HTTP status และข้อความใด และต้องตรวจผลต่อรายการจองและที่นั่งอย่างไร (spec ยังไม่ได้บอก)
- คำตอบของทีม: ยังไม่มีในรอบนี้
- ผล test: ไม่ได้รัน เพราะโหมดร่างต้องหยุดก่อนเขียนโค้ด test ตาม .claude/commands/testcases.md
- ไม่แก้โค้ดระบบหรือ test เดิม

---

## 2569-10-14 คำสั่ง: /testcases AC-BKG-01 specs/001-booking/ (ตามภาพ)

- โหมด: เขียน test จาก 4 แถวสถานะใช้ได้ในตารางจริง
- เพิ่ม test หลังบ้าน TC-BKG-01-1, TC-BKG-01-3, TC-BKG-01-4 ต่อท้าย test เดิม; จำนวน test ใน test_AC_BKG_01.py เพิ่มจาก 1 เป็น 4
- เพิ่ม test หน้าจอ TC-BKG-01-2 จำนวน 1 ตัว แบบ skipped ไม่มี assert เพราะ Then รอ Q-02 และ T-06 ยังรอคำตอบ
- ผล pytest -v ทั้งหลังบ้าน: 6 passed, 1 failed (test เดิม 4 ตัวผ่าน)
- test_TC_BKG_01_1_book_last_seat: PASSED ตรวจรายการจองที่บันทึกและ remaining เป็น 0
- test_TC_BKG_01_3_full_slot: FAILED: assert 201 == 409
- test_TC_BKG_01_4_unverified_user: PASSED ตรวจการปฏิเสธก่อนเข้าถึงบริการ โดยไม่กำหนด status ที่แน่นอนหรือผลต่อข้อมูลที่ spec ไม่ได้บอก
- สาเหตุกรณี 0 ที่: backend/app/booking/service.py บรรทัด 26 ใช้ slot.remaining < 0 จึงยอมให้จองเมื่อเหลือ 0 ที่; ส่วน 3 ช่วงทดแทนยังไม่ถึง assert และเป็นงาน T-05 ที่ยังไม่ทำ
- ผลตรงภาพในพฤติกรรมทั้ง 3 กรณีและข้อความ assert 201 == 409 แต่ชื่อและ ID ใช้ตามตารางจริงที่มีแถวหน้าจอเพิ่ม
- ผล npm test: 1 passed, 1 skipped และ 1 failed suite จาก frontend/tests/researchFilter.test.mjs ที่ใช้ node:test และ Vitest รายงาน No test suite found
- ติดตั้ง dependencies หน้าจอตาม package.json โดยไม่สร้าง lockfile; ไม่แก้โค้ดระบบหรือ test เดิม ไม่ commit/push

---

## 2569-10-14 คำสั่ง: แก้เฉพาะ service.py ให้ปฏิเสธการจองเมื่อไม่มีที่นั่ง ตามภาพ แล้วรัน pytest -v ห้ามแก้ test

- แก้ backend/app/booking/service.py บรรทัด 26 จาก slot.remaining < 0 เป็น slot.remaining <= 0 เท่านั้น
- ไม่แก้ test ใดในรอบนี้; TC กรณีไม่มีที่นั่งในตารางจริงคือ TC-BKG-01-3 (ภาพเรียก TC-BKG-01-2)
- ผล pytest -v: 6 passed, 1 failed
- test_TC_BKG_01_3_full_slot ผ่านการตรวจ HTTP 409 และไม่มีรายการจองแล้ว จึงยืนยันว่าปฏิเสธการจองเมื่อ remaining เป็น 0
- ยังไม่ผ่านการตรวจ 3 ช่วงทดแทน: assert [] == [2, 3, 4] เพราะ router ยังไม่ส่งช่วงทดแทนตาม FR-BKG-03 (T-05 ยังไม่ทำ)
- หยุดตามขอบเขตที่ให้แก้การปฏิเสธเมื่อไม่มีที่นั่ง; ไม่เพิ่มช่วงทดแทน ไม่แก้ router ไม่แก้ test ไม่ commit/push

---

## 2569-10-14 คำสั่ง: แก้ไขรายละเอียด testcase TC-BKG-01-3 ตามภาพ

- ผู้ใช้กำหนดรายละเอียดใหม่โดยตรง: ทางผิด; Given ยังไม่ได้ยืนยันตัวตน และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่; When ยืนยันการจองช่วง 09.00 น.; Then ปฏิเสธตอบ 401 ไม่มีการจอง และที่นั่งว่างยังเป็น 1
- แก้เฉพาะแถว TC-BKG-01-3 ใน test-cases.md พร้อมชื่อ test เป็น test_TC_BKG_01_3_not_verified ให้สอดคล้องกับกรณีใหม่
- คงแถวอื่นตามเดิม รวมถึง TC-BKG-01-4 ซึ่งมี Given คล้ายกัน
- ยังไม่แก้โค้ด test: test_TC_BKG_01_3_full_slot เดิมจึงยังเป็นกรณีไม่มีที่นั่งและไม่ตรงแถวที่เปลี่ยนในรอบนี้
- ไม่แก้โค้ดระบบ ไม่รัน test เพราะเป็นการแก้เอกสาร และไม่ commit/push

---

## 2569-10-14 คำสั่ง: แก้โค้ด test ให้ตรงรายละเอียด testcase ใหม่

- ผู้ใช้อนุญาตให้ปรับ test ตามแถว TC-BKG-01-3 ที่แก้ไขไว้ โดยไม่ได้เปลี่ยนข้อคาดหวังเพื่อให้โค้ดระบบผ่าน
- เปลี่ยน test_TC_BKG_01_3_full_slot เป็น test_TC_BKG_01_3_not_verified: Given ไม่มีผลยืนยันตัวตน ช่วง 09.00 น. ว่าง 1 ที่; When ส่ง POST /bookings โดยไม่มี Authorization; Then ตรวจ 401 ไม่มีรายการจอง และ remaining ยังเป็น 1
- จำนวน test หลังบ้านยังเป็น 7 ตัว; test อื่นและโค้ดระบบไม่เปลี่ยน
- ผล pytest -v: 7 passed, 1 warning ใน 0.89 วินาที; warning มาจาก Starlette เรื่อง httpx
- กรณีที่นั่งเต็มและช่วงทดแทน 3 ช่วงไม่ได้ถูกตรวจโดย TC-BKG-01-3 อีกต่อไป เพราะผู้ใช้เปลี่ยนกรณีทดสอบนี้เป็นกรณีไม่ยืนยันตัวตน
- ไม่ commit/push

---

## 2569-10-14 คำสั่ง: ตรวจการแก้ service.py ตามภาพ แล้วรัน pytest -v ห้ามแก้ test

- ตรวจพบว่า service.py บรรทัด 26 ใช้ slot.remaining <= 0 อยู่แล้ว จึงไม่ต้องแก้ซ้ำ
- ตรวจ commit 8efbea5 ยืนยันว่าโค้ดระบบแก้เพียงบรรทัดเดียวจาก < 0 เป็น <= 0
- ผล pytest -v: 7 passed, 1 warning ใน 0.87 วินาที
- รอบนี้ไม่แก้ test หรือโค้ดระบบ; git diff app/ ว่าง เพราะการแก้เงื่อนไขถูก commit แล้ว
- test ปัจจุบันไม่มีกรณีที่นั่งเหลือ 0 หลังผู้ใช้เปลี่ยน TC-BKG-01-3 เป็นกรณีไม่ยืนยันตัวตน ผล 7 passed จึงไม่ยืนยันกรณีที่นั่ง 0 โดยตรง

---

## 2569-10-14 คำสั่ง: ปรับ Given/When/Then ของ 3 แถวให้ตรงภาพ

- ผู้ใช้ยืนยันให้ปรับทั้ง Given/When/Then ของ TC-BKG-01-1 ถึง TC-BKG-01-3
- TC-BKG-01-1: จองที่นั่งสุดท้าย บันทึก 1 รายการ ที่นั่งเป็น 0 และแสดงหมายเลขคิว (รอ Q-02)
- TC-BKG-01-2: เปลี่ยนจากหน้าจอเป็นกรณีขอบ ที่นั่งเหลือ 0 ตอบ 409 ไม่มีการจองใหม่ และที่นั่งยังเป็น 0 ไม่ติดลบ; ตรวจด้วย pytest ชื่อ test_TC_BKG_01_2_no_seat_left
- TC-BKG-01-3: ตรวจข้อความแล้วตรงภาพอยู่แล้ว คือยังไม่ยืนยันตัวตน ตอบ 401 ไม่มีการจอง และที่นั่งยังเหลือ 1
- คง TC-BKG-01-4 ไว้ เพราะไม่ได้รับคำสั่งให้ลบ; การแสดงหมายเลขคิวระบุการตรวจหน้าจอที่ TC-BKG-01-1 และยังรอ Q-02
- แก้เฉพาะเอกสาร ไม่แก้โค้ด test หรือระบบ และไม่รัน test; โค้ด test TC-BKG-01-2 ยังต้องปรับตามตารางใหม่ในรอบถัดไป

---

## 2569-10-14 คำสั่ง: ทดสอบ testcase ทั้งหมดใหม่

- รัน test ทั้งหลังบ้านและหน้าจอ: หลังบ้านเดิม 7 passed; หน้าจอ 1 passed, 1 skipped และ 1 failed suite จาก researchFilter.test.mjs (No test suite found)
- พบ TC-BKG-01-2 ตามตารางล่าสุดยังไม่มีโค้ด จึงเพิ่ม test_TC_BKG_01_2_no_seat_left โดยคง test เดิมทั้งหมด
- Given ผู้รับบริการอีกคนจองที่สุดท้ายแล้ว When ผู้ที่ยืนยันตัวตนส่งคำขอจอง Then ตอบ 409 ไม่เพิ่มการจองและที่นั่งยังเป็น 0
- ผล pytest -v หลังเพิ่มกรณีที่ขาด: 8 passed, 1 warning ใน 0.95 วินาที
- ปรับเฉพาะคอมเมนต์และชื่อกรณีหน้าจอที่ข้ามให้ระบุ TC-BKG-01-1 ตามตารางล่าสุด; การแสดงเลขคิวยังรอ Q-02
- ไม่แก้โค้ดระบบ ไม่แก้ suite researchFilter ไม่ commit/push
