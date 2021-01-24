import markdown
from markdown.extensions import fenced_code

md = '''
You will be provided with a set of numbers, read from the **stdin**. Your task is to print the result to the **stdout**.

## Input:

- On the first line you will receive the number *N*
- On the following *N* lines, you will receive a number
  - A number from the set

## Output

- On the single line of the output, print the sum of the set of numbers

## Sample input:

```
5
1
2
3
4
5
```

## Sample output:

```
15
```
'''

result = markdown.markdown(md, extensions=['fenced_code'])
print(result)