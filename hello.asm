org 100h
mov ax,cs
mov es,ax
mov ax,6
mov si,files
int 22h
push eax
push si
mov ax,06000h
mov es,ax
mov bx,0
pop si
pop ecx
push si
mov ax,7
int 22h
pop si
mov ax,cs
mov es,ax
mov ax,8
int 22h
mov ax,13h
int 10h
mov ax,cs
mov es,ax
mov ax,3
mov bx,cmds
int 22h
mov ax,0
int 21h
int 20
ret
ret
cmds db "hello.c32",0
files db "bitmap.raw",0
endf db 0
