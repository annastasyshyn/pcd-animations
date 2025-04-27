import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.animation import FuncAnimation, FFMpegWriter
from scipy.fft import fft2, ifft2, fftshift, ifftshift
from tqdm import tqdm
import pathlib

N = 100
CUTOFF = 0.16
Z_EXAG = 1.8

x = np.linspace(-1, 1, N)
y = np.linspace(-1, 1, N)
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2)

Z_clean = np.zeros_like(R)
inside = R <= 1
Z_clean[inside] = np.sqrt(1 - R[inside]**2)

Z_clean -= Z_clean.min()
Z_clean *= Z_EXAG / Z_clean.max()

np.random.seed(0)
noise = 0.4 * np.random.randn(N, N)
Z_noisy = Z_clean + noise * inside
Z_noisy -= Z_noisy.min()
Z_noisy *= Z_EXAG / Z_noisy.max()

F      = fftshift(fft2(Z_noisy))
u      = np.arange(N) - N/2
v      = u[:, None]
radius = np.sqrt(u**2 + v**2)
mask   = radius < (CUTOFF * N)
F_filt = F * mask

Z_deno = np.real(ifft2(ifftshift(F_filt)))
Z_deno -= Z_deno.min()
Z_deno *= Z_EXAG / Z_deno.max()

amp      = np.log(np.abs(F) + 1e-9)
amp      = (amp - amp.min()) / (amp.max() - amp.min())
amp_filt = np.log(np.abs(F_filt) + 1e-9)
amp_filt = (amp_filt - amp_filt.min()) / (amp_filt.max() - amp_filt.min())

plt.style.use("dark_background")
fig = plt.figure(figsize=(10, 6))
gs  = fig.add_gridspec(2, 2, height_ratios=[3, 1], width_ratios=[3, 2])

ax3d  = fig.add_subplot(gs[:, 0], projection='3d')
ax_spec = fig.add_subplot(gs[0, 1])
ax_tl   = fig.add_subplot(gs[1, 1])
ax_tl.axis("off")

ax_spec.set_xticks([]); ax_spec.set_yticks([])

surf = ax3d.plot_surface(
    X, Y, Z_noisy,
    rcount=100, ccount=100,
    cmap=cm.viridis,
    linewidth=0,
    antialiased=False,
    alpha=1.0
)
im_spec = ax_spec.imshow(amp, cmap='gray', origin='lower', alpha=0.0)

mask_circle = plt.Circle((N/2, N/2), 0,
                         fc='none', ec='yellow', lw=2, alpha=1.0)
ax_spec.add_patch(mask_circle)

title = ax3d.set_title("", fontsize=16)

ax3d.set_xlabel("X"); ax3d.set_ylabel("Y"); ax3d.set_zlabel("Z")
ax3d.set_zlim(0, Z_EXAG)

TOTAL_FRAMES = 200

def update(frame):
    t = frame / TOTAL_FRAMES
    if t < 0.2:
        title.set_text("Noisy hemisphere")
    elif t < 0.4:
        k = (t - 0.2) / 0.2
        surf.set_alpha(1 - k)
        im_spec.set_alpha(k)
        title.set_text("2D FFT amplitude")
    elif t < 0.6:
        k = (t - 0.4) / 0.2
        mask_circle.set_radius(k * CUTOFF * N)
        title.set_text("Apply low-pass filter")
    elif t < 0.8:
        k = (t - 0.6) / 0.2
        im_spec.set_data((1 - k) * amp + k * amp_filt)
        title.set_text("Filtered spectrum")
    else:
        k = (t - 0.8) / 0.2
        Z_interp = (1 - k) * Z_noisy + k * Z_deno
        ax3d.clear()
        ax3d.plot_surface(
            X, Y, Z_interp,
            rcount=100, ccount=100,
            cmap=cm.viridis,
            linewidth=0,
            antialiased=False
        )
        ax3d.set_zlim(0, Z_EXAG)
        ax3d.set_xlabel("X"); ax3d.set_ylabel("Y"); ax3d.set_zlabel("Z")
        title.set_text("Denoised hemisphere")
    return surf, im_spec, mask_circle, title

anim = FuncAnimation(fig, update, frames=TOTAL_FRAMES, blit=False)

out = pathlib.Path("hemisphere_denoise.mp4")
writer = FFMpegWriter(
    fps=30,
    codec='libx264',
    extra_args=['-pix_fmt', 'yuv420p']
)

pbar = tqdm(total=TOTAL_FRAMES, desc="Rendering frames", unit="frame")
def progress_callback(current, total):
    pbar.update(1)

anim.save(str(out), writer=writer, progress_callback=progress_callback)
pbar.close()

print(f"Animation saved to {out.resolve()}")
