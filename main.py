
import registrar
import shell

if __name__ == "__main__":
    registrar.loginRoutine()
    if(registrar.verifyUser()):
        shell.openShell()