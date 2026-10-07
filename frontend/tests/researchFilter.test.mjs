import test from 'node:test'
import assert from 'node:assert/strict'
import { filterResearches } from '../src/researchFilter.ts'
const items=[{id:1,title:'หนึ่ง',contract:'ABC',lead:'สมชาย',keywords:['Clean Water'],sdgs:[6,9],status:'กำลังดำเนินการ'},{id:2,title:'สอง',contract:'DEF',lead:'สมหญิง',keywords:['Water'],sdgs:[6],status:'โครงการเสร็จสิ้น'},{id:3,title:'สาม',contract:'GHI',lead:'อื่น',status:'กำลังดำเนินการ'}]
const base={query:'',status:'ทั้งหมด',keyword:'',sdgs:[],match:'any'}
test('search includes hidden keywords and researchers with trimmed case-insensitive input',()=>{
  assert.deepEqual(filterResearches(items,{...base,query:' CLEAN '}).map(x=>x.id),[1])
  assert.deepEqual(filterResearches(items,{...base,query:'สมหญิง'}).map(x=>x.id),[2])
  assert.equal(filterResearches(items,base).length,3)
})
test('SDGs support any or all and combine with keyword and status',()=>{
  assert.deepEqual(filterResearches(items,{...base,sdgs:[6,9]}).map(x=>x.id),[1,2])
  assert.deepEqual(filterResearches(items,{...base,sdgs:[6,9],match:'all'}).map(x=>x.id),[1])
  assert.deepEqual(filterResearches(items,{...base,sdgs:[6],keyword:'water',status:'โครงการเสร็จสิ้น'}).map(x=>x.id),[2])
  assert.deepEqual(filterResearches(items,{...base,keyword:'missing'}),[])
})
