import string
import secrets
  
def gen_rand_string(len):
  alphabet = string.ascii_letters + string.digits
  return ''.join(secrets.choice(alphabet) for i in range(len))
