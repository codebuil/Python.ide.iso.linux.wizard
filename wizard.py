import tkinter as tk
import subprocess
import os
from tkinter import filedialog

def clear_text():
    text.delete('1.0', tk.END)

def execute_command(command):
    
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
    clear_text()
    text.insert(tk.END, "create dir project /tmp/cd/ ....\r\n")
    execute_command("rm -rf /tmp/cd")
    execute_command("mkdir -p /tmp/cd")
    # execute_command("mkdir -p /tmp/cd/isolinux")
    execute_command("mkdir -p /tmp/cd/images")
    execute_command("mkdir -p /tmp/cd/kernel")
    execute_command("unzip -u -q isolinux.zip -d /tmp/cd/")
    text.insert(tk.END, "done\r\n")

def create_asm_com():
    text.insert(tk.END, "compile asm com...\r\n")
    input_file = filedialog.askopenfilename(filetypes=[("Assembly Files", "*.asm *.s")])
    text.insert(tk.END, input_file+"\r\n")
    output_file = os.path.splitext(os.path.basename(input_file))[0]
    execute_command(f"nasm \"{input_file}\" -o {output_file}.com")
    execute_command(f"mv {output_file}.com /tmp/cd/isolinux")
    text.insert(tk.END, "done\r\n")

def create_com32_asm():
    text.insert(tk.END, "compile asm com32...\r\n")
    input_file = filedialog.askopenfilename(filetypes=[("Assembly Files", "*.asm *.s")])
    text.insert(tk.END, input_file+"\r\n")
    output_file = os.path.splitext(os.path.basename(input_file))[0]
    execute_command(f"nasm  \"{input_file}\" -o {output_file}.c32")
    execute_command(f"mv {output_file}.c32 /tmp/cd/isolinux")
    text.insert(tk.END, "done\r\n")

def create_bcc_exec():
    text.insert(tk.END, "compile bcc com ...\r\n")
    input_file = filedialog.askopenfilename(filetypes=[("C Files", "*.c")])
    text.insert(tk.END, input_file+"\r\n")
    output_file = os.path.splitext(os.path.basename(input_file))[0]
    execute_command(f"bcc -c -Md libdos.c -o libdos.a")
    execute_command(f"bcc -x -i -L \"{input_file}\" {output_file}.com")
    execute_command(f"mv {output_file}.com /tmp/cd/isolinux")
    text.insert(tk.END, "done\r\n")

def nasm_elf32():
    text.insert(tk.END, "compile gcc com32 ...\r\n")
    input_file = filedialog.askopenfilename(filetypes=[("C Files", "*.c")])
    output_file = os.path.splitext(os.path.basename(input_file))[0]
    text.insert(tk.END, input_file+"\r\n")
    execute_command(f"nasm -felf32 boot.S -o boot.o")
    execute_command(f"gcc -c \"{input_file}\" -o {output_file}.o -nostdlib")
    
    execute_command(f"gcc link.ld boot.o {output_file}.o -o {output_file}.elf -nostdlib")
    execute_command(f"nasm model.asm -o model.o")
    execute_command(f"dd if={output_file}.elf of={output_file}.c32")
    execute_command(f"dd if=model.o of={output_file}.c32 count=1 conv=notrunc")
    execute_command(f"mv {output_file}.c32 /tmp/cd/isolinux")
    text.insert(tk.END, "done\r\n")


def create_iso_image():
    text.insert(tk.END, "creat iso image ...\r\n")
    execute_command("cp isolinux.cfg /tmp/cd/isolinux")
    execute_command("genisoimage -o myos.iso -input-charset utf-8 -b isolinux/isolinux.bin -no-emul-boot -boot-load-size 4 -boot-info-table /tmp/cd")

    execute_command("rm *.o")
    execute_command("rm *.elf")
    execute_command("rm *.com")
    execute_command("rm *.c32")
    text.insert(tk.END, "done\r\n")
def copy_isolinux_cfg():
    text.insert(tk.END, "add a txt file a raw or binary ...\r\n")
    input_file = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
    text.insert(tk.END, input_file+"\r\n")
    output_file = f"/tmp/isolinux/output.com"
    execute_command(f"cp \"{input_file}\" /tmp/cd/isolinux")
    text.insert(tk.END, "done\r\n")

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
