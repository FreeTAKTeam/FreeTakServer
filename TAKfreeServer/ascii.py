import sys
import time
import os

def slowprint(s):
    for c in s + '\n' :
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(1. / 500)
def ascii()
    slowprint(r'''\
    *** ***       FREE TAK SERVER        *** ***       
                .------.
               /  ~ ~   \,------.      ______
             ,'  ~ ~ ~  /  (@)   \   ,'      \
           ,'          /`.    ~ ~ \ /         \
         ,'           | ,'\  ~ ~ ~ X     \  \  \
       ,'  ,'          V--<       (       \  \  \
     ,'  ,'               (vv      \/\  \  \  |  |
    (__,'  ,'   /         (vv   ""    \  \  | |  |
      (__,'    /   /       vv   """    \ |  / / /
          \__,'   /  |     vv          / / / / /
              \__/   / |  | \         / /,',','
                 \__/\_^  |  \       /,'',','\
                        `-^.__>.____/  ' ,'   \
                                // //---'      |
              ===============(((((((=================
                                         | \ \  \
                                         / |  |  \
                                        / /  / \  \
                                        `.     |   \
                                          `--------'

         - The parrot's not dead! It's just resting!- 
    ''')
