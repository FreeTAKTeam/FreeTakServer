import sys
import time

class AsciiController:
  def slowprint(self, s):
      for c in s + '\n' :
          print(c)
          time.sleep(1. / 400)
  def ascii(self):
      self.slowprint(r'''\
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
