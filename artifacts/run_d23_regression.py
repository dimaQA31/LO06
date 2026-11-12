import json,subprocess,sys
from pathlib import Path
import stand
original=stand.profile()
record={'previous_settings':original,'runs':[]}
try:
 for profile in ['clean','lesson-06']:
  result=subprocess.run([sys.executable,'cli.py','--set','l06_security','--profile',profile,'--gate','all','--traces','--brief'],check=False)
  record['runs'].append({'profile':profile,'exit_code':result.returncode})
  if result.returncode not in (0,1): break
finally:
 record['restored_settings']=stand.set_profile(original['profile'])
 Path('artifacts/d23_regression_execution.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
 print('Profile restored: '+original['profile'],flush=True)
