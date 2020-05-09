# run by
# pypara -p example1.py
# pypara -p example1.py -g "1 2 3"
# pypara -p example1.py -r "echo {f}"

generator = range(3)

def run(i):
    print(i)
