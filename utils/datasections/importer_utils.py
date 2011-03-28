
def clean_value(val):
  if    val.lower() == 'true':  return True
  elif  val.lower() == 'false': return False
  else:                         return val.strip()
