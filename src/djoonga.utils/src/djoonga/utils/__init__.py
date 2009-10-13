import subprocess

def jconfig(var):
    "Return value of project's JConfig->var"
    cmd = ['php','-r','''include('html/configuration.php'); $config = new JConfig; echo $config->%s;'''%var]
    s = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output, error = s.communicate()
    return output