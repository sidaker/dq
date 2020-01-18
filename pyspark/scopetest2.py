global_var = 1
def my_vars():
  print("Global Variable:", global_var)
  # global_var = global_var + 1 # UnboundLocalError: local variable 'global_var' referenced before assignment
  local_var = 2
  print("Local Variable:",local_var )
  global global_inner_var
  global_inner_var = 1

my_vars()
print("Coerced Global:", global_inner_var)
