# Always non default arguments should precede default arguments
def echo(lang,user='Likhi',sys='Linux'):
    print('User:',user,'Language:','Platform:',sys)

def fibinocci_gen():
    a = b = 1
    while True:
        yield a
        a, b = b, a + b

echo('Sid','Python','Mac')
echo(lang='Java',user='Bargu',sys='Windows')
echo(lang='Scala')

fib = fibinocci_gen()

for i in fib:
    assert type(i) is int, 'Argument must be Integer'
    if i > 100:
        break
    else:
        print('Generated:',i)
