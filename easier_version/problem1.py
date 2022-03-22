def number_stream(str_param):
  # format input
  num_list = list(map(int, str_param.strip()))

  sequence = []
  for number in num_list:
    if not sequence:
      sequence.append(number)
    elif number in sequence:
      sequence.append(number)
      if len(sequence) == number:
        return True
    else:
      sequence = []
      sequence.append(number)

  # code goes here
  return False

# keep this function call here 
print(number_stream(input()))

# Example input: '2315647777777890'

