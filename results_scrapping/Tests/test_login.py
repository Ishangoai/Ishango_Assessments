import pytest

# Completely random tests below

bad_result = 'test failed'

def test_file1_method1():
	x=5
	y=6
	assert x+1 == y, bad_result

def test_file1_method2():
	x=5
	y=6
	assert x+1 == y, bad_result
