# 入力
FizzBuzzのコードを書いてください。

# 出力(ChatGPT)
もちろんです！以下はPythonでのFizzBuzzのコード例です。

```python
for i in range(1, 101):
    if i % 3 == 0 and i % 5 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)
```

このコードは1から100までの数字を順に処理し、以下の条件に基づいて出力します：

- もし数字が3で割り切れる場合、"Fizz"と出力します。
- もし数字が5で割り切れる場合、"Buzz"と出力します。
- もし数字が3でも5でも割り切れる場合、"FizzBuzz"と出力します。
- 上記のいずれの条件にも当てはまらない場合、その数字を出力します。

このコードを実行すると、以下のような出力が得られます：

```
1
2
Fizz
4
Buzz
Fizz
7
8
Fizz
Buzz
11
Fizz
13
14
FizzBuzz
16
...
98
Fizz
Buzz
```

これはFizzBuzzの問題を解くための基本的なコードです。他のプログラミング言語でも同様のアプローチでFizzBuzzを実装することができます。