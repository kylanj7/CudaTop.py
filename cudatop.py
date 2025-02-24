import curses
import pynvml
import time
import random

def init_gpus():
    pynvml.nvmlInit()
    num_gpus = pynvml.nvmlDeviceGetCount()
    return [pynvml.nvmlDeviceGetHandleByIndex(i) for i in range(num_gpus)]

def get_gpu_info(handle):
    name = pynvml.nvmlDeviceGetName(handle)
    if isinstance(name, bytes):
        name = name.decode('utf-8')
    utilization = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
    memory = pynvml.nvmlDeviceGetMemoryInfo(handle)
    core_count = pynvml.nvmlDeviceGetNumGpuCores(handle)
    return name, utilization, memory, core_count

def draw_cuda_cores(stdscr, cores, usage, start_y, start_x, max_width, max_height):
    cores_per_row = max_width // 4  # Each core representation takes 4 characters [XX]
    rows = min(max_height - start_y, cores // cores_per_row + (1 if cores % cores_per_row else 0))
    
    for i in range(min(cores, rows * cores_per_row)):
        row = i // cores_per_row
        col = i % cores_per_row
        y = start_y + row
        x = start_x + col * 4

        if y < max_height and x < max_width - 4:
            core_usage = min(100, max(0, usage + random.randint(-10, 10)))  # Add some randomness
            if core_usage > 75:
                color = curses.color_pair(1)  # Red
            elif core_usage > 25:
                color = curses.color_pair(2)  # Yellow
            else:
                color = curses.color_pair(3)  # Green

            stdscr.addstr(y, x, f"[{core_usage:2d}]", color)

def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)  # Non-blocking input
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

    gpu_handles = init_gpus()

    try:
        while True:
            stdscr.clear()
            height, width = stdscr.getmaxyx()

            for i, gpu_handle in enumerate(gpu_handles):
                name, utilization, memory, core_count = get_gpu_info(gpu_handle)
                mem_used = memory.used / 1024**2
                mem_total = memory.total / 1024**2

                info_str = f"GPU {i}: {name} | Utilization: {utilization}% | Memory: {mem_used:.0f}/{mem_total:.0f} MB | Cores: {core_count}"
                stdscr.addstr(i*4, 0, info_str[:width-1])
                stdscr.addstr(i*4+1, 0, "=" * (width - 1))

                draw_cuda_cores(stdscr, core_count, utilization, i*4+2, 0, width, height)

            stdscr.addstr(height-1, 0, "Press 'q' to quit", curses.A_REVERSE)
            stdscr.refresh()
            time.sleep(1)
            
            if stdscr.getch() == ord('q'):
                break
    except KeyboardInterrupt:
        pass
    finally:
        pynvml.nvmlShutdown()

if __name__ == "__main__":
    curses.wrapper(main)