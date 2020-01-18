global_var = 1
def my_vars():
  print("Global Variable:", global_var) # See how it is different to below
  # global_var = global_var + 1 # UnboundLocalError: local variable 'global_var' referenced before assignment
  # Variables with global scope can be referenced inside a function
  local_var = 2 # the scope of the variable is purely local.
  print("Local Variable:",local_var )
  global global_inner_var
  global_inner_var = 1

my_vars()
print("Coerced Global:", global_inner_var)
