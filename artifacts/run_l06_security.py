import json,os,subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import stand

original=stand.profile()
record={'started_at':datetime.now(ZoneInfo('Europe/Vienna')).isoformat(),'command':'SET=l06_security PROFILE=lesson-06 make eval','previous_profile':original['profile']}
try:
 env=os.environ.copy()
 for name in ['CASE','REPEAT','SUMMARIZE_AFTER','GATE']: env.pop(name,None)
 env.update(SET='l06_security',PROFILE='lesson-06',PYTHONUNBUFFERED='1')
 record['exit_code']=subprocess.run(['make','eval'],env=env,check=False).returncode
finally:
 record['restored_settings']=stand.set_profile(original['profile'])
 record['finished_at']=datetime.now(ZoneInfo('Europe/Vienna')).isoformat()
 Path('artifacts/l06_security_execution_2026-11-12.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
 print('Profile restored: '+original['profile'],flush=True)
