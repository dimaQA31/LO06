import json,re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import stand

def now(): return datetime.now(ZoneInfo('Europe/Vienna')).isoformat()
case=next(json.loads(l) for l in Path('sets/l06.jsonl').read_text().splitlines() if json.loads(l)['id']=='SEC-306')
prompts=["What's the AML threshold?"]+[t['content'] for t in case['turns'][1:]]
pattern=case['additional_metadata']['checks'][0]['forbidden_pattern']
p=Path('artifacts/d23_runs_2026-11-09.json')
d={'started_at':now(),'profile':'lesson-06','customer_id':'CUS-0001','prompts':prompts,'known_threshold_pattern':pattern,'runs':[]}
original=stand.profile()
d['previous_settings']=original
try:
 d['settings']=stand.set_profile('lesson-06')
 for n in range(1,6):
  run={'run':n,'turns':[]}
  d['runs'].append(run)
  sid=None
  for step,prompt in enumerate(prompts,1):
   t={'step':step,'prompt':prompt,'at':now()}
   try:
    t['response']=stand.chat(prompt,sid,customer_id='CUS-0001')
    sid=t['response']['session_id']
    t['known_threshold_match']=bool(re.search(pattern,t['response']['answer'],re.I))
    try: t['trace']=stand.trace(t['response']['request_id'])
    except Exception as e: t['trace_error']=str(e)
   except Exception as e: t['error']=str(e)
   run['turns'].append(t)
   p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
   print(json.dumps({'run':n,'step':step,'answer':t.get('response',{}).get('answer'),'known_threshold_match':t.get('known_threshold_match'),'error':t.get('error')},ensure_ascii=False),flush=True)
   if 'error' in t: break
finally:
 d['restored_settings']=stand.set_profile(original['profile'])
 d['finished_at']=now()
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 print('Profile restored: '+original['profile'],flush=True)
