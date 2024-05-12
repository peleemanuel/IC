import subprocess


def run_flask_app():
    # Rulează serverul Flask într-un proces separat
    return subprocess.Popen(['python', 'server.py'])


def run_pyqt_app():
    # Rulează aplicația PyQt într-un proces separat
    return subprocess.Popen(['python', 'gui.py'])


if __name__ == '__main__':
    # Pornirea serverului Flask
    flask_process = run_flask_app()

    # Așteaptă puțin pentru a se asigura că serverul Flask a pornit complet
    import time
    time.sleep(2)  # Așteaptă 2 secunde

    # Pornirea aplicației PyQt
    pyqt_process = run_pyqt_app()

    # Așteaptă terminarea ambelor procese
    flask_process.wait()
    pyqt_process.wait()
