from io import StringIO
import sys
import eel

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout

@eel.expose
def get_code(code, arg):
    success = 0
    for i in arg:
        with Capturing() as output:
            def test(*args):
                a = args[0]
                b = args[1]
                c = args[2]
                
                try:
                    exec(code)
                except:
                    print("Ошибка")

            test(*i[0])
            
        if i[1] == output:
            print("Success")
        else:
            success += 1
            print("Wrong")

    return [output, success]

eel.init("web")
eel.start("index.html")