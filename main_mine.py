import pygame, os

pygame.font.init()
pygame.mixer.init()

LARGURA_TELA, ALTURA_TELA = 900, 500
TELA = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Joguinho de Navinha pew pew pew")

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
AMARELO = (255, 255, 0)

BORDA = pygame.Rect(LARGURA_TELA//2 - 5, 0, 10, ALTURA_TELA)

SOM_HIT = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
SOM_TIRO = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

FONTE_HP = pygame.font.SysFont('comicsans', 40)

FONTE_VITORIA = pygame.font.SysFont('comicsans', 100)

FPS = 60

VEL = 5

VEL_BALA =  10

MAX_BALAS = 3

LARGURA_NAVE, ALTURA_NAVE = 55, 40

HIT_AMARELO = pygame.USEREVENT + 1
HIT_VERMELHO = pygame.USEREVENT + 2

NAVE_AMARELA_IMG = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
NAVE_AMARELA = pygame.transform.rotate(pygame.transform.scale(NAVE_AMARELA_IMG, (LARGURA_NAVE, ALTURA_NAVE)), 90)

NAVE_VERMELHA_IMG = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
NAVE_VERMELHA = pygame.transform.rotate(pygame.transform.scale(NAVE_VERMELHA_IMG, (LARGURA_NAVE, ALTURA_NAVE)), 270)

ESPACO = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (LARGURA_TELA, ALTURA_TELA))

def desenhar_na_tela(vermelho, amarelo, balas_vermelho, balas_amarelo, hp_vermelho, hp_amarelo):
    TELA.blit(ESPACO, (0,0))
    
    pygame.draw.rect(TELA, PRETO, BORDA)
    
    texto_hp_vermelho = FONTE_HP.render("HP: " + str(hp_vermelho), 1, BRANCO)
    texto_hp_amarelo = FONTE_HP.render("HP: " + str(hp_amarelo), 1, BRANCO)
    
    TELA.blit(texto_hp_vermelho, (LARGURA_TELA - texto_hp_vermelho.get_width()  - 10, 10))
    TELA.blit(texto_hp_amarelo, (10, 10))
    
    TELA.blit(NAVE_AMARELA, (amarelo.x, amarelo.y))
    TELA.blit(NAVE_VERMELHA, (vermelho.x, vermelho.y))
    
    for bala in balas_vermelho:
        pygame.draw.rect(TELA, VERMELHO, bala)
    
    for bala in balas_amarelo:
        pygame.draw.rect(TELA, AMARELO, bala)
        
    
    pygame.display.update()

def movimento_amarelo(teclas_pressionadas, amarelo):  
    if teclas_pressionadas[pygame.K_a] and amarelo.x - VEL > 0: #esquerda
        amarelo.x -= VEL
    if teclas_pressionadas[pygame.K_d] and amarelo.x + VEL + amarelo.width < BORDA.x: #direita
        amarelo.x += VEL
    if teclas_pressionadas[pygame.K_w] and amarelo.y - VEL > 0: #cima
        amarelo.y -= VEL
    if teclas_pressionadas[pygame.K_s] and amarelo.y + VEL + amarelo.height < ALTURA_TELA - 15: #baixo
        amarelo.y += VEL
        
def movimento_vermelho(teclas_pressionadas, vermelho):  
    if teclas_pressionadas[pygame.K_LEFT] and vermelho.x - VEL > BORDA.x + BORDA.width: #esquerda
        vermelho.x -= VEL
    if teclas_pressionadas[pygame.K_RIGHT] and vermelho.x + VEL + vermelho.width < LARGURA_TELA: #direita
        vermelho.x += VEL
    if teclas_pressionadas[pygame.K_UP] and vermelho.y - VEL > 0: #cima
        vermelho.y -= VEL
    if teclas_pressionadas[pygame.K_DOWN] and vermelho.y + VEL + vermelho.height < ALTURA_TELA - 15: #baixo
        vermelho.y += VEL

def funcionamento_balas(balas_amarelo, balas_vermelho, amarelo, vermelho):
    for bala in balas_amarelo:
        bala.x += VEL_BALA
        if vermelho.colliderect(bala):
            pygame.event.post(pygame.event.Event(HIT_VERMELHO))
            balas_amarelo.remove(bala)
        elif bala.x > LARGURA_TELA:
            balas_amarelo.remove(bala)

    for bala in balas_vermelho:
        bala.x -= VEL_BALA
        if amarelo.colliderect(bala):
            pygame.event.post(pygame.event.Event(HIT_AMARELO))
            balas_vermelho.remove(bala)
        elif bala.x < 0:
            balas_vermelho.remove(bala)

def mostrar_vitoria(texto):
    texto_vitoria = FONTE_VITORIA.render(texto, 1, BRANCO)
    TELA.blit(texto_vitoria, (LARGURA_TELA/2 - texto_vitoria.get_width()/2, ALTURA_TELA/2 - texto_vitoria.get_height()/2))
    
    pygame.display.update()
    
    pygame.time.delay(5000)

def main():
    vermelho = pygame.Rect(700, 300, LARGURA_NAVE, ALTURA_NAVE)
    amarelo = pygame.Rect(100, 300, LARGURA_NAVE, ALTURA_NAVE)
    
    balas_vermelho = []
    balas_amarelo = []
    
    hp_vermelho = 10
    hp_amarelo = 10
    
    clock = pygame.time.Clock()
    
    terminou = False
    while (not terminou):
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminou = True
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(balas_amarelo) < MAX_BALAS:
                    bala = pygame.Rect(amarelo.x + amarelo.width, amarelo.y + amarelo.height//2 + 2.5, 10, 5)
                    balas_amarelo.append(bala)
                    SOM_TIRO.play()
                
                if event.key == pygame.K_RCTRL and len(balas_vermelho) < MAX_BALAS:
                    bala = pygame.Rect(vermelho.x, vermelho.y + vermelho.height//2 + 2.5, 10, 5)
                    balas_vermelho.append(bala)
                    SOM_TIRO.play()
                    
            if event.type == HIT_VERMELHO:
                hp_vermelho -= 1
                SOM_HIT.play()
            
            if event.type == HIT_AMARELO:
                hp_amarelo -= 1
                SOM_HIT.play()
        
        texto_vencedor = ""
        
        if hp_vermelho <= 0:
            texto_vencedor = "Amarelo venceu!"
        
        if hp_amarelo <= 0:
            texto_vencedor = "Vermelho venceu!"
        
        if texto_vencedor != "":
            mostrar_vitoria(texto_vencedor)
            break

        teclas_pressionadas = pygame.key.get_pressed()
        movimento_amarelo(teclas_pressionadas, amarelo)
        movimento_vermelho(teclas_pressionadas, vermelho)
        
        funcionamento_balas(balas_amarelo, balas_vermelho, amarelo, vermelho)
        
        desenhar_na_tela(vermelho, amarelo, balas_vermelho, balas_amarelo, hp_vermelho, hp_amarelo)
    
    main()

if __name__ == "__main__":
    main()