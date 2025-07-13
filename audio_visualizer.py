import pygame
import numpy as np
import sounddevice as sd

WIDTH, HEIGHT = 800, 400
FPS = 60
BAR_COUNT = 64  # Not used in new visualization

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Audio Visualizer")
clock = pygame.time.Clock()

# Audio settings
SAMPLERATE = 44100
BLOCKSIZE = 1024

def audio_callback(indata, frames, time, status):
    global audio_data
    # Apply smoothing to reduce sensitivity
    new_data = np.copy(indata[:, 0])
    audio_data = 0.8 * audio_data + 0.2 * new_data




# For heart rate monitor style waveform
audio_data = np.zeros(BLOCKSIZE)
waveform = np.zeros(WIDTH)
stream = sd.InputStream(callback=audio_callback, channels=1, samplerate=SAMPLERATE, blocksize=BLOCKSIZE)
stream.start()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((10, 10, 20))

    # Get amplitude from audio and apply scaling
    amplitude = np.abs(audio_data).mean()
    amplitude = np.log1p(amplitude) * 350  # increased multiplier for more dramatic amplitude change

    # Scroll waveform left and add new value
    waveform = np.roll(waveform, -1)
    # Add a pulse effect based on amplitude
    waveform[-1] = amplitude + np.random.normal(0, 2)

    # Draw a glowing, color-gradient heart rate monitor style waveform
    points = [(x, HEIGHT//2 - int(waveform[x])) for x in range(WIDTH)]
    if len(points) > 1:
        # Draw glow by drawing thicker, transparent lines behind
        for glow in range(8, 0, -2):
            color = (0, 255//glow, 128//glow, 40)
            surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pygame.draw.lines(surf, color, False, points, glow)
            screen.blit(surf, (0, 0))
        # Draw main line with color gradient
        for i in range(1, len(points)):
            c = int(255 * i / WIDTH)
            color = (c, 255-c, 128)
            pygame.draw.line(screen, color, points[i-1], points[i], 2)

    # Optionally, draw a grid for style
    for y in range(HEIGHT//4, HEIGHT, HEIGHT//4):
        pygame.draw.line(screen, (30, 30, 60), (0, y), (WIDTH, y), 1)

    pygame.display.flip()
    clock.tick(FPS)

stream.stop()
pygame.quit()
