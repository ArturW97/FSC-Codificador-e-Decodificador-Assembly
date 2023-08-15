 .text   
 .globl  main            
         
 main:  la	$t0,A		# Carrega endereco de A em $t0 - PSEUDO-INSTRUCAO
 	lw	$t1,0($t0)	# Le valor de A para $t1
 	la	$t2,B		# Carrega endereco de B em $t2 - PSEUDO-INSTRUCAO
 	lw	$t3,0($t2)	# Le valor de B para $t3
 	addiu	$t4,$t1,4	# $t4 recebe A+B
 	andi	$t4,$t1,4	# $t4 recebe A+B
	srl		$t4,$t1,4	# $t4 recebe A+B
	sll 	$t3,$t3,2
	lw		$s2,0($t0)
	sw		$s2,0($t0)
 	la	$t5,C		# Carrega endereco de C em $t5 - PSEUDO-INSTRUCAO
 	sw	$t4,0($t5)	# C recebe A+B
 	
 	
 	
 	li	$v0, 10   
 	syscall
 	
 	
 	
 	.data
 A:	.word	1
 B:	.word	2
 C:	.word	0

        
 
 