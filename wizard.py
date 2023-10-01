import tkinter as tk
import subprocess
import os
from tkinter import filedialog

def clear_text():
    text.delete('1.0', tk.END)

def execute_command(command):
    clear_text()
    try:
        result = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output = result.stdout
        errors = result.stderr
        text.insert(tk.END, output)
        text.insert(tk.END, errors)
    except Exception as e:
        text.insert(tk.END, f"Erro: {str(e)}")

def create_project():
    execute_command("rm -rf /tmp/cd")
    execute_command("mkdir -p /tmp/cd")
    # execute_command("mkdir -p /tmp/cd/isolinux")
    execute_command("mkdir -p /tmp/cd/images")
    execute_command("mkdir -p /tmp/cd/kernel")
    execute_command("unzip -u -q isolinux.zip -d /tmp/cd/")

def create_asm_com():
    input_file = filedialog.askopenfilename(filetypes=[("Assembly Files", "*.asm *.s")])
    output_file = os.path.splitext(os.path.basename(input_file))[0]
    execute_command(f"nasm \"{input_file}\" -o {output_file}.com")
    execute_command(f"mv {output_file}.com /tmp/cd/isolinux")

def create_com32_asm():
    input_file = filedialog.askopenfilename(filetypes=[("Assembly Files", "*.asm *.s")])
    output_file = os.path.splitext(os.path.basename(input_file))[0]
    execute_command(f"nasm  \"{input_file}\" -o {output_file}.c32")
    execute_command(f"mv {output_file}.c32 /tmp/cd/isolinux")


def create_bcc_exec():
    input_file = filedialog.askopenfilename(filetypes=[("C Files", "*.c")])
    output_file = os.path.splitext(os.path.basename(input_file))[0]
    execute_command(f"bcc -c -Md libdos.c -o libdos.a")
    execute_command(f"bcc -x -i -L \"{input_file}\" {output_file}.com")
    execute_command(f"mv {output_file}.com /tmp/cd/isolinux")

def nasm_elf32():
    input_file = filedialog.askopenfilename(filetypes=[("C Files", "*.c")])
    output_file = os.path.splitext(os.path.basename(input_file))[0]
    execute_command(f"nasm -felf32 boot.S -o boot.o")
    execute_command(f"gcc -c \"{input_file}\" -o {output_file}.o -nostdlib")
    
    execute_command(f"gcc link.ld boot.o {output_file}.o -o {output_file}.elf -nostdlib")
    execute_command(f"nasm model.asm -o model.o")
    execute_command(f"dd if={output_file}.elf of={output_file}.c32")
    execute_command(f"dd if=model.o of={output_file}.c32 count=1 conv=notrunc")
    execute_command(f"mv {output_file}.c32 /tmp/cd/isolinux")


def create_iso_image():
    execute_command("genisoimage -o myos.iso -input-charset utf-8 -b isolinux/isolinux.bin -no-emul-boot -boot-load-size 4 -boot-info-table /tmp/cd")
    execute_command("cp isolinux.cfg /tmp/cd/isolinux")
    execute_command("genisoimage -o myos.iso -input-charset utf-8 -b isolinux/isolinux.bin -no-emul-boot -boot-load-size 4 -boot-info-table /tmp/cd")
    execute_command("cp isolinux.cfg /tmp/cd/isolinux")
    execute_command("rm *.o")
    execute_command("rm *.elf")
    execute_command("rm *.com")
    execute_command("rm *.c32")
def copy_isolinux_cfg():
    input_file = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
    output_file = f"/tmp/isolinux/output.com"
    execute_command(f"cp \"{input_file}\" /tmp/cd/isolinux")


def qemu_run():
    execute_command("qemu-system-i386 -serial msmouse -cdrom myos.iso")

# Cria a janela principal
root = tk.Tk()
root.title("Linux Debian Helper")
root.configure(bg="blue")# Cria a área de texto


# Cria os botões
buttons = [
    ("Create Project", create_project),
    ("Create asm.com", create_asm_com),
    ("Create com32.asm", create_com32_asm),
    ("Create bcc exec", create_bcc_exec),
    ("gcc .c32", nasm_elf32),
    ("Create ISO Image", create_iso_image),
    ("copy raw files", copy_isolinux_cfg),
    ("Run QEMU", qemu_run),
]

for button_text, command in buttons:
    button = tk.Button(root, text=button_text, command=command)
    button.pack()
text = tk.Text(root)
text.pack(fill=tk.BOTH, expand=True)
root.mainloop()
