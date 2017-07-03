#! usr/bin/python3
''' *** Proyecto Primer Parcial Sistemas Operativos ***
    Monitor de senales 
'''
import sys
import subprocess
import psutil


def isfloat(num):
    try:
        float(num)
        return True
    except Exception:
        return False


def call_free():
    ''' Return dictionary with the info of free command
    '''
    output = {}
    result = subprocess.run(['free'], stdout=subprocess.PIPE)
    data = result.stdout.decode('utf-8').split('\n')[1].split()
    output['total'] = data[1]
    output['used'] = data[2]
    output['free'] = data[3]
    output['shared'] = data[4]
    output['buf/cache'] = data[5]
    output['avaliable'] = data[6]
    return output


def is_full_memory(MAX_MEM):
    ''' Return boolean, True if the memory is bigger than MAX_MEM
    '''
    response = call_free()
    use_percent = (int(
        response['total']) - int(response['avaliable'])) * 100 / int(response['total'])
    if use_percent >= int(MAX_MEM):
        return True
    else:
        return False


def get_memory_status():
    ''' Return the memory usage percent
    '''
    response = call_free()
    use_percent = (int(
        response['total']) - int(response['avaliable'])) * 100 / int(response['total'])
    return use_percent


def get_usage_cpu():
    '''Return % usage cpu
    Reference:
    https://github.com/Leo-G/DevopsWiki/wiki/How-Linux-CPU-Usage-Time-and-Percentage-is-calculated

    cat /proc/stat
        user nice system idle iowait  irq  softirq steal guest guest_nice
    cpu  4705 356  584    3699   23    23     0       0     0          0

    Total CPU time since boot = user+nice+system+idle+iowait+irq+softirq+steal

    Total CPU Idle time since boot = idle + iowait

    Total CPU usage time since boot = Total CPU time since boot - Total CPU Idle time since boot

    Total CPU percentage = Total CPU usage time since boot/Total CPU time since boot X 100
    '''

    # result = subprocess.run(['cat', '/proc/stat'], stdout=subprocess.PIPE)
    # info = result.stdout.decode('utf-8').split('\n')[0].split()
    # tctsb = int(info[1]) + int(info[2]) + int(info[3]) + int(info[4]) + \
    #     int(info[5]) + int(info[6]) + int(info[7]) + int(info[8])
    # tcitsb = int(info[4]) + int(info[5])
    # tcutsb = tctsb - tcitsb
    # usage_cpu = tcutsb / tctsb * 100
    # return usage_cpu
    return psutil.cpu_percent(interval=1)


def call_ps():
    ''' Return 
    '''
    # usedr, pid, %cpu, %men, vsz, rss, tty, stat, start, time, command
    output = []
    result = subprocess.run(['ps', 'aux'], stdout=subprocess.PIPE)
    data = result.stdout.decode('utf-8').split('\n')
    for linea in data:
        tmp = linea.split()
        output.append(tmp)
    return output


def search_by_cpu_usage(MAX_CPU):
    processes = []
    for process in call_ps():
        try:
            if float(process[2]) >= float(MAX_CPU):
                processes.append(process)
        except (IndexError, ValueError):
            pass
    return processes


def search_by_memory_usage(MEM_BY_PROCESS):
    processes = []
    for process in call_ps():
        try:
            if float(process[3]) >= float(MEM_BY_PROCESS):
                processes.append(process)
        except Exception as e:
            pass
    return processes


def stop_process(PID):
    subprocess.run(['kill', '-19', PID])


def continue_process(PID):
    subprocess.run(['kill', '-18', PID])


def kill_process(PID):
    subprocess.run(['kill', '-9', PID])


def monitor_cpu(MAX_CPU, OK_CPU, CPU_USAGE):
    '''MAX_CPU %  max de uso del cpu permitido por proceso
    OK_CPU apartir de que % reactiva procesos
    MAX_MEN % max de uso del cpu'''
    hungry_cpu = search_by_cpu_usage(MAX_CPU)
    if CPU_USAGE > float(OK_CPU):
        print("CPU al {}% en busca de procesos que usen {}%".format(
            CPU_USAGE, MAX_CPU))
        for process in hungry_cpu:
            print("Proceso consumiendo mucho CPU:")
            print("Suspendiendo de proceso .....")
            print(process)
            stop_process(process[1])
            print("======================================")
    else:
        print("Uso del CPU por debajo de OK_CPU:{}%".format(OK_CPU))
        if hungry_cpu:
            for process in hungry_cpu:
                # preguntar por el estado del proceso
                '''
                T    stopped, either by a job control signal or because it is being traced
                '''
                if "T" in process[7]:
                    print("Reanudando procesos suspendidos......")
                    print(process)
                    continue_process(process[1])
                    print("======================================")
            hungry_cpu = []
        else:
            print("No hay procesos consumiendo CPU en exceso")
            print("======================================")
            hungry_cpu = []


def monitor_mem(MAX_MEM, MEM_BY_PROCESS):
    if is_full_memory(MAX_MEM):
        hungry_mem = search_by_memory_usage(MEM_BY_PROCESS)
        for process in hungry_mem:
            print("Proceso ocupando {}% o mas siendo detenido......".format(
                MEM_BY_PROCESS))
            print(process)
            kill_process(process[1])
            print("======================================")
    else:
        print("Memoria estable....")
        print("======================================")


def monitor(MAX_CPU, OK_CPU, MAX_MEM):
    cpu_usage = get_usage_cpu()
    print("CPU AL {}%".format(cpu_usage))
    print("Memoria al {0:.2f}%".format(get_memory_status()))
    monitor_cpu(MAX_CPU, OK_CPU, cpu_usage)
    monitor_mem(MAX_MEM, '10')


if __name__ == '__main__':
    MAX_CPU = sys.argv[1]
    OK_CPU = sys.argv[2]
    MAX_MEM = sys.argv[3]
    if isfloat(MAX_CPU) and isfloat(OK_CPU) and isfloat(MAX_MEM):
        print("Iniciando monitoreo ....")
        while True:
            monitor(MAX_CPU, OK_CPU, MAX_MEM)
    else:
        print("Parametros incorrectos, ingrese nuevamente")
