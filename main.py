import random
# import fish
import params

def main():
    print("Starting FishyML...")

if __name__ == "__main__":
    main()

x = "global"

def foo():
 print(params.WINDOW_LENGTH)
 params.WINDOW_LENGTH = 200
 
foo()
print('outside')
print(params.WINDOW_LENGTH)
