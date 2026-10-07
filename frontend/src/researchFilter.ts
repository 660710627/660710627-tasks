import type { Research } from './research'

export type ResearchFilter = { query:string; status:string; keyword:string; sdgs:number[]; match:'any'|'all' }
export function filterResearches(items:Research[], filter:ResearchFilter):Research[] {
  const normalize=(value:string)=>value.trim().toLocaleLowerCase()
  const query=normalize(filter.query), keyword=normalize(filter.keyword)
  return items.filter(item=>{
    const words=item.keywords??[]
    const text=[item.title,item.contract,item.lead,item.leader?.name??'',item.collaborators??'',...(item.coResearchers??[]).map(member=>member.name),...words].map(normalize)
    return (!query||text.some(value=>value.includes(query)))
      && (filter.status==='ทั้งหมด'||item.status===filter.status)
      && (!keyword||words.some(value=>normalize(value).includes(keyword)))
      && (!filter.sdgs.length||(filter.match==='all'?filter.sdgs.every(id=>item.sdgs?.includes(id)):filter.sdgs.some(id=>item.sdgs?.includes(id))))
  })
}
