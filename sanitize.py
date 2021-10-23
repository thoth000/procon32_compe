import sys

def sanitize(s, target):
    new_s = ''
    queue = ''
    for c in s:
        if c == target[0]:
            queue += c
        elif len(queue) and c == target[1]:
            queue = queue[:-1]
        else:
            new_s += queue
            queue = ''

            new_s += c

    new_s += queue

    return new_s

def main():
    s = []
    with open(sys.argv[1], 'r') as f:
        s = f.read().split('\n')

    print(s[3])
    while True:
        last_len = len(s[4])
        s[4] = sanitize(sanitize(sanitize(sanitize(s[4], 'UD'), 'DU'), 'LR'), 'RL')

        print(s[3])
        if last_len == len(s[4]):
            break

        s[3] = str(len(s[4]))

    for i in range(len(s)):
        s[i] += '\n'

    with open(sys.argv[1], 'w') as f:
        f.writelines(s)

main()